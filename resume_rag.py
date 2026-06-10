"""
resume_rag.py - The Resume Ingestion Engine

This script handles the heavy lifting of reading resumes, breaking them down into 
manageable pieces, and storing them so we can search through them later. 

Here's the general flow:
- Grab resumes from the disk
- Slice them up intelligently (we don't want to cut a sentence in half!)
- Turn the text into vector embeddings 
- Save everything into our local ChromaDB
- Ask Gemini to pull out the key details (like names, skills, and experience)

Usage:
    python resume_rag.py --index          # Read and save all resumes
    python resume_rag.py --query "..."    # Do a quick semantic search test
    python resume_rag.py --stats          # Check how many resumes we have saved
    python resume_rag.py --reset          # Wipe the database and start fresh
"""

import argparse
import json
import os
import re
import sys
import time
import hashlib
import textwrap
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from config import (
    RESUME_DIR, CHROMA_DB_PATH, CHROMA_COLLECTION_NAME,
    EMBEDDING_PROVIDER, HF_EMBEDDING_MODEL, HF_EMBEDDING_DIM,
    OPENAI_EMBEDDING_MODEL, OPENAI_EMBEDDING_DIM,
    CHUNK_MAX_CHARS, CHUNK_OVERLAP_CHARS, SUPPORTED_EXTENSIONS,
    GEMINI_MODEL, TOP_K,
)
from fs_tools import read_file, list_files


# ═══════════════════════════════════════════════════════════════
# 1. RESUME CHUNKER — Section-aware splitting
# ═══════════════════════════════════════════════════════════════

class ResumeChunker:
    """
    Splits resume text into meaningful chunks that preserve section context.

    Strategy:
    - Detect section headers (SKILLS, EXPERIENCE, EDUCATION, etc.)
    - Each section becomes one chunk
    - If a section exceeds CHUNK_MAX_CHARS, split on paragraph boundaries
    - Always produce a 'full_resume' summary chunk for holistic matching
    """

    SECTION_HEADERS = [
        "PROFESSIONAL SUMMARY", "SUMMARY", "OBJECTIVE", "PROFILE",
        "SKILLS", "TECHNICAL SKILLS", "CORE COMPETENCIES",
        "WORK EXPERIENCE", "EXPERIENCE", "EMPLOYMENT HISTORY", "EMPLOYMENT",
        "EDUCATION", "ACADEMIC BACKGROUND", "ACADEMIC",
        "CERTIFICATIONS", "CERTIFICATES", "LICENSES",
        "PROJECTS", "KEY PROJECTS", "PERSONAL PROJECTS",
        "PUBLICATIONS", "RESEARCH",
        "ACHIEVEMENTS", "AWARDS",
    ]

    def __init__(self, max_chars: int = CHUNK_MAX_CHARS, overlap: int = CHUNK_OVERLAP_CHARS):
        self.max_chars = max_chars
        self.overlap = overlap
        # Build regex pattern for header detection
        # Matches lines that are mostly uppercase and match known headers
        escaped = [re.escape(h) for h in self.SECTION_HEADERS]
        self.header_pattern = re.compile(
            r"^\s*(" + "|".join(escaped) + r")\s*$",
            re.IGNORECASE | re.MULTILINE,
        )

    def chunk_resume(self, text: str, filename: str) -> list[dict]:
        """
        Split resume into section-based chunks.

        Returns list of dicts, each with:
            - text: chunk content
            - section: section name (e.g. 'SKILLS', 'WORK EXPERIENCE')
            - filename: source resume filename
            - chunk_index: sequential index within this resume
            - chunk_type: 'section' or 'full_resume'
        """
        chunks = []

        # ── Step 1: Extract name (usually the first non-empty line) ──
        lines = text.strip().splitlines()
        candidate_name = ""
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith(("Email", "Phone", "LinkedIn", "Location", "GitHub", "Portfolio")):
                candidate_name = stripped
                break

        # ── Step 2: Find section boundaries ──
        sections = self._split_into_sections(text)

        # ── Step 3: Create section chunks ──
        chunk_index = 0
        for section_name, section_text in sections:
            section_text = section_text.strip()
            if not section_text:
                continue

            # If section is within limit, keep as-is
            if len(section_text) <= self.max_chars:
                chunks.append({
                    "text": section_text,
                    "section": section_name,
                    "filename": filename,
                    "candidate_name": candidate_name,
                    "chunk_index": chunk_index,
                    "chunk_type": "section",
                })
                chunk_index += 1
            else:
                # Split large sections on paragraph/bullet boundaries
                sub_chunks = self._split_large_section(section_text)
                for sub in sub_chunks:
                    chunks.append({
                        "text": sub,
                        "section": section_name,
                        "filename": filename,
                        "candidate_name": candidate_name,
                        "chunk_index": chunk_index,
                        "chunk_type": "section",
                    })
                    chunk_index += 1

        # ── Step 4: Add full resume chunk (truncated if very long) ──
        full_text = text.strip()
        if len(full_text) > self.max_chars * 2:
            full_text = full_text[: self.max_chars * 2] + "\n[...truncated...]"

        chunks.append({
            "text": full_text,
            "section": "FULL_RESUME",
            "filename": filename,
            "candidate_name": candidate_name,
            "chunk_index": chunk_index,
            "chunk_type": "full_resume",
        })

        return chunks

    def _split_into_sections(self, text: str) -> list[tuple[str, str]]:
        """Split text into (section_name, section_content) tuples."""
        matches = list(self.header_pattern.finditer(text))

        if not matches:
            # No recognizable headers — return entire text as one section
            return [("GENERAL", text)]

        sections = []

        # Content before the first header (contact info, name, etc.)
        preamble = text[: matches[0].start()].strip()
        if preamble:
            sections.append(("CONTACT_INFO", preamble))

        # Each header and its following content
        for i, match in enumerate(matches):
            section_name = match.group(1).upper().strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            content = text[start:end].strip()
            sections.append((section_name, content))

        return sections

    def _split_large_section(self, text: str) -> list[str]:
        """Split a large section into sub-chunks on paragraph boundaries."""
        paragraphs = re.split(r"\n\s*\n", text)

        chunks = []
        current = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current) + len(para) + 2 <= self.max_chars:
                current = current + "\n\n" + para if current else para
            else:
                if current:
                    chunks.append(current)
                current = para

        if current:
            chunks.append(current)

        return chunks if chunks else [text]


# ═══════════════════════════════════════════════════════════════
# 2. EMBEDDING GENERATOR — Multi-provider support
# ═══════════════════════════════════════════════════════════════

class EmbeddingGenerator:
    """
    Generates embeddings using either HuggingFace sentence-transformers
    (free, local) or OpenAI API (paid, higher quality).
    """

    def __init__(self, provider: str = EMBEDDING_PROVIDER):
        self.provider = provider.lower()

        if self.provider == "huggingface":
            self._init_huggingface()
        elif self.provider == "openai":
            self._init_openai()
        else:
            raise ValueError(f"Unknown embedding provider: {provider}. Use 'huggingface' or 'openai'.")

    def _init_huggingface(self):
        """Initialize HuggingFace sentence-transformers model."""
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            print("Error: sentence-transformers not installed.")
            print("Run: pip install sentence-transformers")
            sys.exit(1)

        print(f"  Loading HuggingFace model: {HF_EMBEDDING_MODEL} ...")
        self.model = SentenceTransformer(HF_EMBEDDING_MODEL)
        self.dim = HF_EMBEDDING_DIM
        print(f"  [OK] Model loaded (dim={self.dim})")

    def _init_openai(self):
        """Initialize OpenAI embedding client."""
        try:
            from openai import OpenAI
        except ImportError:
            print("Error: openai package not installed.")
            print("Run: pip install openai")
            sys.exit(1)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not set.")
            sys.exit(1)

        self.client = OpenAI(api_key=api_key)
        self.dim = OPENAI_EMBEDDING_DIM
        print(f"  [OK] OpenAI client ready (model={OPENAI_EMBEDDING_MODEL}, dim={self.dim})")

    def generate(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        if self.provider == "huggingface":
            return self._generate_hf(texts)
        else:
            return self._generate_openai(texts)

    def _generate_hf(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings using HuggingFace."""
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        return embeddings.tolist()

    def _generate_openai(self, texts: list[str], batch_size: int = 100) -> list[list[float]]:
        """Generate embeddings using OpenAI API with batching."""
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = self.client.embeddings.create(
                model=OPENAI_EMBEDDING_MODEL,
                input=batch,
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
            time.sleep(0.1)  # rate limiting

        return all_embeddings


# ═══════════════════════════════════════════════════════════════
# 3. METADATA EXTRACTOR — LLM-powered + regex fallback
# ═══════════════════════════════════════════════════════════════

class MetadataExtractor:
    """
    Extracts structured metadata from resume text using Gemini LLM.
    Falls back to regex-based extraction if LLM is unavailable.
    """

    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
        self.model = None

        if use_llm:
            try:
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
                if api_key:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel(GEMINI_MODEL)
                    print("  [OK] Gemini model ready for metadata extraction")
                else:
                    print("  No Gemini API key found — using regex fallback")
                    self.use_llm = False
            except ImportError:
                print("  google-generativeai not installed — using regex fallback")
                self.use_llm = False

    def extract(self, resume_text: str, filename: str) -> dict:
        """
        Extract structured metadata from resume text.

        Returns:
            {
                "candidate_name": str,
                "skills": list[str],
                "experience_years": int,
                "education": list[dict],  # {"degree": ..., "institution": ..., "year": ...}
                "current_role": str,
                "location": str,
                "email": str,
            }
        """
        if self.use_llm and self.model:
            try:
                return self._extract_with_llm(resume_text, filename)
            except Exception as e:
                print(f"    LLM extraction failed for {filename}: {e}")
                return self._extract_with_regex(resume_text, filename)
        else:
            return self._extract_with_regex(resume_text, filename)

    def _extract_with_llm(self, resume_text: str, filename: str) -> dict:
        """Use Gemini to extract structured metadata."""
        prompt = f"""Extract the following information from this resume and return ONLY a valid JSON object (no markdown, no code fences):

{{
    "candidate_name": "Full name of the candidate",
    "skills": ["skill1", "skill2", ...],
    "experience_years": <total years of professional experience as integer>,
    "education": [
        {{"degree": "degree name", "institution": "university name", "year": "graduation year"}}
    ],
    "current_role": "most recent job title",
    "location": "city, state",
    "email": "email address"
}}

RESUME:
{resume_text[:3000]}
"""
        response = self.model.generate_content(prompt)
        text = response.text.strip()

        # Clean up potential markdown fences
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)

        metadata = json.loads(text)

        # Ensure all fields exist
        metadata.setdefault("candidate_name", "")
        metadata.setdefault("skills", [])
        metadata.setdefault("experience_years", 0)
        metadata.setdefault("education", [])
        metadata.setdefault("current_role", "")
        metadata.setdefault("location", "")
        metadata.setdefault("email", "")

        return metadata

    def _extract_with_regex(self, resume_text: str, filename: str) -> dict:
        """Regex-based fallback extraction."""
        lines = resume_text.strip().splitlines()

        # ── Name: first non-empty, non-contact line ──
        candidate_name = ""
        for line in lines:
            stripped = line.strip()
            if stripped and not any(kw in stripped.lower() for kw in
                                   ["email", "phone", "linkedin", "github", "location", "portfolio", "@"]):
                candidate_name = stripped
                break

        # ── Email ──
        email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", resume_text)
        email = email_match.group() if email_match else ""

        # ── Location ──
        loc_match = re.search(r"Location:\s*(.+)", resume_text, re.IGNORECASE)
        location = loc_match.group(1).strip() if loc_match else ""

        # ── Skills ──
        skills = self._extract_skills_regex(resume_text)

        # ── Experience years ──
        experience_years = self._estimate_experience_years(resume_text)

        # ── Education ──
        education = self._extract_education_regex(resume_text)

        # ── Current role ──
        current_role = self._extract_current_role(resume_text)

        return {
            "candidate_name": candidate_name,
            "skills": skills,
            "experience_years": experience_years,
            "education": education,
            "current_role": current_role,
            "location": location,
            "email": email,
        }

    def _extract_skills_regex(self, text: str) -> list[str]:
        """Extract skills from the SKILLS section."""
        skills_section = re.search(
            r"(?:SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES)\s*\n(.*?)(?=\n\s*(?:WORK EXPERIENCE|EXPERIENCE|EDUCATION|CERTIFICATIONS|PROJECTS|PUBLICATIONS|$))",
            text, re.IGNORECASE | re.DOTALL
        )
        if not skills_section:
            return []

        section_text = skills_section.group(1)
        skills = []

        # Parse "Category: skill1, skill2, skill3" patterns
        for line in section_text.splitlines():
            line = line.strip()
            if ":" in line:
                _, _, skill_part = line.partition(":")
                for s in re.split(r"[,;|]", skill_part):
                    s = s.strip().strip("•-")
                    if s and len(s) > 1:
                        skills.append(s)
            elif line.startswith(("•", "-", "*")):
                s = line.lstrip("•-* ").strip()
                if s and len(s) > 1:
                    skills.append(s)

        return skills

    def _estimate_experience_years(self, text: str) -> int:
        """Estimate total years of experience from date ranges."""
        # Look for patterns like "Jun 2017 – Present" or "2019 – 2022"
        date_ranges = re.findall(
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*(\d{4})\s*[–—-]\s*(?:(Present)|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*(\d{4}))",
            text, re.IGNORECASE
        )

        if not date_ranges:
            # Try "X years of experience" pattern
            years_match = re.search(r"(\d+)\+?\s*years?\s*(?:of\s+)?experience", text, re.IGNORECASE)
            return int(years_match.group(1)) if years_match else 0

        # Find earliest start and latest end
        starts = []
        ends = []
        for start_year, is_present, end_year in date_ranges:
            starts.append(int(start_year))
            if is_present:
                ends.append(2025)
            elif end_year:
                ends.append(int(end_year))

        if starts and ends:
            return max(ends) - min(starts)
        return 0

    def _extract_education_regex(self, text: str) -> list[dict]:
        """Extract education entries."""
        education = []
        # Pattern: "B.Tech Computer Science — IIT Bombay (2018)"
        edu_pattern = re.findall(
            r"((?:B\.?Tech|M\.?Tech|B\.?Sc|M\.?Sc|B\.?Com|M\.?Com|MBA|B\.?Des|M\.?A|Ph\.?D)[\w\s,&/()]+?)(?:—|–|-)\s*(.+?)\s*\((\d{4})\)",
            text
        )
        for degree, institution, year in edu_pattern:
            education.append({
                "degree": degree.strip(),
                "institution": institution.strip(),
                "year": year.strip(),
            })
        return education

    def _extract_current_role(self, text: str) -> str:
        """Extract the most recent job title."""
        # Look for pattern: "Title — Company, Location"
        role_match = re.search(
            r"(?:WORK EXPERIENCE|EXPERIENCE)\s*\n\s*\n?\s*(.+?)(?:—|–|-)\s*",
            text, re.IGNORECASE
        )
        return role_match.group(1).strip() if role_match else ""


# ═══════════════════════════════════════════════════════════════
# 4. VECTOR STORE — ChromaDB wrapper
# ═══════════════════════════════════════════════════════════════

class ResumeVectorStore:
    """
    ChromaDB-based vector store for resume chunks.
    Supports persistent storage, metadata filtering, and semantic queries.
    """

    def __init__(self, persist_dir: str = CHROMA_DB_PATH, collection_name: str = CHROMA_COLLECTION_NAME):
        try:
            import chromadb
        except ImportError:
            print("Error: chromadb not installed. Run: pip install chromadb")
            sys.exit(1)

        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        print(f"  [OK] ChromaDB ready (path={persist_dir}, collection={collection_name})")

    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]],
                   resume_metadata: dict):
        """
        Store chunks with their embeddings and metadata.

        Args:
            chunks: list of chunk dicts from ResumeChunker
            embeddings: corresponding embedding vectors
            resume_metadata: extracted metadata for the resume
        """
        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:
            # Create unique ID from filename + chunk index
            chunk_id = hashlib.md5(
                f"{chunk['filename']}_{chunk['chunk_index']}".encode()
            ).hexdigest()

            ids.append(chunk_id)
            documents.append(chunk["text"])

            # Flatten metadata for ChromaDB (supports str, int, float, bool)
            meta = {
                "filename": chunk["filename"],
                "section": chunk["section"],
                "chunk_index": chunk["chunk_index"],
                "chunk_type": chunk["chunk_type"],
                "candidate_name": resume_metadata.get("candidate_name", ""),
                "experience_years": resume_metadata.get("experience_years", 0),
                "current_role": resume_metadata.get("current_role", ""),
                "location": resume_metadata.get("location", ""),
                "skills": ", ".join(resume_metadata.get("skills", [])),
                "email": resume_metadata.get("email", ""),
            }
            metadatas.append(meta)

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(self, query_embedding: list[float], n_results: int = TOP_K,
              where_filter: Optional[dict] = None) -> dict:
        """
        Query the vector store with a query embedding.

        Returns ChromaDB query results with documents, distances, and metadatas.
        """
        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": n_results,
            "include": ["documents", "distances", "metadatas"],
        }
        if where_filter:
            kwargs["where"] = where_filter

        return self.collection.query(**kwargs)

    def get_stats(self) -> dict:
        """Get collection statistics."""
        count = self.collection.count()
        # Get unique filenames
        if count > 0:
            all_data = self.collection.get(include=["metadatas"])
            filenames = set(m["filename"] for m in all_data["metadatas"])
            return {
                "total_chunks": count,
                "total_resumes": len(filenames),
                "filenames": sorted(filenames),
            }
        return {"total_chunks": 0, "total_resumes": 0, "filenames": []}

    def reset(self):
        """Delete and recreate the collection."""
        import chromadb
        self.client.delete_collection(CHROMA_COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        print("  [OK] Collection reset")


# ═══════════════════════════════════════════════════════════════
# 5. RAG PIPELINE — Full indexing pipeline
# ═══════════════════════════════════════════════════════════════

class ResumeRAGPipeline:
    """
    End-to-end pipeline: load resumes → chunk → embed → store in ChromaDB.
    """

    def __init__(self):
        print("\nWaking up the Resume Ingestion Pipeline...\n")
        self.chunker = ResumeChunker()
        self.embedder = EmbeddingGenerator()
        self.store = ResumeVectorStore()
        self.extractor = MetadataExtractor(use_llm=True)
        print()

    def index_all_resumes(self, resume_dir: str = str(RESUME_DIR)) -> dict:
        """
        Load, chunk, embed, and store all resumes from the directory.

        Returns summary statistics.
        """
        print(f"Loading resumes from: {resume_dir}\n")

        # List all resume files
        result = list_files(resume_dir)
        if not result["success"]:
            print(f"Error listing files: {result['error']}")
            return {"error": result["error"]}

        files = [f for f in result["files"]
                 if os.path.splitext(f["name"])[1].lower() in SUPPORTED_EXTENSIONS]

        if not files:
            print("No resume files found!")
            return {"error": "No resume files found"}

        print(f"  Found {len(files)} resume files\n")

        total_chunks = 0
        all_stats = []
        start_time = time.time()

        for i, file_info in enumerate(files, 1):
            filename = file_info["name"]
            filepath = file_info["path"]
            print(f"  [{i}/{len(files)}] Processing: {filename}")

            # ── Load ──
            read_result = read_file(filepath)
            if not read_result["success"]:
                print(f"    Skipping (read error): {read_result['error']}")
                continue

            resume_text = read_result["content"]
            if not resume_text or len(resume_text.strip()) < 50:
                print(f"    Skipping (too short or empty)")
                continue

            # ── Extract metadata ──
            metadata = self.extractor.extract(resume_text, filename)
            print(f"    → Name: {metadata['candidate_name']} | "
                  f"Exp: {metadata['experience_years']}y | "
                  f"Skills: {len(metadata['skills'])}")

            # ── Chunk ──
            chunks = self.chunker.chunk_resume(resume_text, filename)
            print(f"    → Chunks: {len(chunks)}")

            # ── Embed ──
            chunk_texts = [c["text"] for c in chunks]
            embeddings = self.embedder.generate(chunk_texts)

            # ── Store ──
            self.store.add_chunks(chunks, embeddings, metadata)
            total_chunks += len(chunks)

            all_stats.append({
                "filename": filename,
                "candidate_name": metadata["candidate_name"],
                "chunks": len(chunks),
                "experience_years": metadata["experience_years"],
                "skills_count": len(metadata["skills"]),
            })

        elapsed = time.time() - start_time
        print(f"\nIndexing complete!")
        print(f"   Resumes: {len(all_stats)} | Chunks: {total_chunks} | Time: {elapsed:.1f}s")

        return {
            "resumes_indexed": len(all_stats),
            "total_chunks": total_chunks,
            "elapsed_seconds": round(elapsed, 2),
            "details": all_stats,
        }

    def search(self, query: str, top_k: int = TOP_K,
               where_filter: Optional[dict] = None) -> list[dict]:
        """
        Semantic search over indexed resumes.

        Returns list of matches with scores and metadata.
        """
        # Generate query embedding
        query_embedding = self.embedder.generate([query])[0]

        # Query ChromaDB
        results = self.store.query(query_embedding, n_results=top_k * 3,
                                   where_filter=where_filter)

        if not results["ids"][0]:
            return []

        # Deduplicate by filename (keep best match per resume)
        seen_files = {}
        for idx in range(len(results["ids"][0])):
            doc_id = results["ids"][0][idx]
            distance = results["distances"][0][idx]
            document = results["documents"][0][idx]
            metadata = results["metadatas"][0][idx]

            filename = metadata["filename"]
            # cosine distance → similarity (1 - distance)
            similarity = max(0, 1.0 - distance)

            if filename not in seen_files or similarity > seen_files[filename]["similarity"]:
                seen_files[filename] = {
                    "filename": filename,
                    "candidate_name": metadata.get("candidate_name", ""),
                    "similarity": round(similarity, 4),
                    "matched_section": metadata.get("section", ""),
                    "excerpt": document[:300] + "..." if len(document) > 300 else document,
                    "experience_years": metadata.get("experience_years", 0),
                    "current_role": metadata.get("current_role", ""),
                    "location": metadata.get("location", ""),
                    "skills": metadata.get("skills", ""),
                }

        # Sort by similarity and return top-K
        matches = sorted(seen_files.values(), key=lambda x: x["similarity"], reverse=True)
        return matches[:top_k]


# ═══════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="RAG-based Resume Processing Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python resume_rag.py --index
              python resume_rag.py --query "Python Django developer with AWS"
              python resume_rag.py --stats
              python resume_rag.py --reset --index
        """),
    )
    parser.add_argument("--index", action="store_true",
                        help="Index all resumes from the resumes/ directory")
    parser.add_argument("--query", type=str,
                        help="Run a semantic search query")
    parser.add_argument("--top-k", type=int, default=TOP_K,
                        help=f"Number of results to return (default: {TOP_K})")
    parser.add_argument("--stats", action="store_true",
                        help="Show index statistics")
    parser.add_argument("--reset", action="store_true",
                        help="Clear the vector store before indexing")

    args = parser.parse_args()

    if not any([args.index, args.query, args.stats, args.reset]):
        parser.print_help()
        return

    pipeline = ResumeRAGPipeline()

    if args.reset:
        print("\nResetting vector store...")
        pipeline.store.reset()
        print()

    if args.index:
        print("\nIndexing all resumes...\n")
        stats = pipeline.index_all_resumes()
        print(f"\nIndex Stats: {json.dumps(stats, indent=2, default=str)}")

    if args.query:
        print(f"\nSearching for: \"{args.query}\"\n")
        start = time.time()
        results = pipeline.search(args.query, top_k=args.top_k)
        elapsed = time.time() - start

        if not results:
            print("  No results found. Have you indexed resumes first? (--index)")
        else:
            for i, match in enumerate(results, 1):
                print(f"  {i}. {match['candidate_name']} — {match['filename']}")
                print(f"     Similarity: {match['similarity']:.4f} | "
                      f"Section: {match['matched_section']} | "
                      f"Exp: {match['experience_years']}y")
                print(f"     Role: {match['current_role']}")
                print(f"     Skills: {match['skills'][:80]}...")
                print()

            print(f"  Search latency: {elapsed * 1000:.0f}ms")

    if args.stats:
        stats = pipeline.store.get_stats()
        print(f"\nVector Store Statistics:")
        print(f"   Total chunks: {stats['total_chunks']}")
        print(f"   Total resumes: {stats['total_resumes']}")
        if stats["filenames"]:
            print(f"   Indexed files:")
            for fn in stats["filenames"]:
                print(f"     - {fn}")


if __name__ == "__main__":
    main()
