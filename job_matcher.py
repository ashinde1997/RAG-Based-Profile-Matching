"""
job_matcher.py - The Matchmaker

This is where we actually find the right people for the job!
It takes a job description, figures out what it's actually asking for, 
and then searches through our database of resumes to find the best fits.

How it does it:
- Reads the JD and pulls out the hard requirements.
- Uses semantic search (understanding the meaning) + keyword search (finding exact skills).
- Scores everyone fairly out of 100 so you can rank them.
- Asks the AI to write a short, human-readable reason why they're a good fit.

Usage:
    python job_matcher.py --jd job_descriptions/jd_senior_python_backend.txt
    python job_matcher.py --jd job_descriptions/jd_ml_engineer.txt --top-k 5
    python job_matcher.py --all --output output/
    python job_matcher.py --interactive
"""

import argparse
import json
import os
import re
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from config import (
    JD_DIR, OUTPUT_DIR, TOP_K,
    WEIGHT_SEMANTIC, WEIGHT_SKILL, WEIGHT_EXPERIENCE, WEIGHT_EDUCATION,
    GEMINI_MODEL, RESUME_DIR,
)
from resume_rag import ResumeRAGPipeline


# ═══════════════════════════════════════════════════════════════
# 1. JOB DESCRIPTION PROCESSOR
# ═══════════════════════════════════════════════════════════════

class JobDescriptionProcessor:
    """
    Parses a job description to extract structured requirements.
    Uses Gemini LLM with regex fallback.
    """

    def __init__(self):
        self.model = None
        try:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(GEMINI_MODEL)
        except Exception:
            pass

    def parse_jd(self, jd_text: str) -> dict:
        """
        Extract structured fields from a job description.

        Returns:
            {
                "title": str,
                "company": str,
                "location": str,
                "min_experience_years": int,
                "required_skills": list[str],
                "preferred_skills": list[str],
                "must_have_requirements": list[str],
                "responsibilities": list[str],
            }
        """
        if self.model:
            try:
                return self._parse_with_llm(jd_text)
            except Exception as e:
                print(f"  LLM JD parsing failed: {e}, using regex fallback")

        return self._parse_with_regex(jd_text)

    def _parse_with_llm(self, jd_text: str) -> dict:
        """Parse JD using Gemini LLM."""
        prompt = f"""Extract the following information from this job description and return ONLY a valid JSON object (no markdown, no code fences):

{{
    "title": "job title",
    "company": "company name",
    "location": "location",
    "min_experience_years": <minimum years of experience as integer>,
    "required_skills": ["skill1", "skill2", ...],
    "preferred_skills": ["skill1", "skill2", ...],
    "must_have_requirements": ["requirement1", "requirement2", ...],
    "responsibilities": ["responsibility1", "responsibility2", ...]
}}

JOB DESCRIPTION:
{jd_text}
"""
        response = self.model.generate_content(prompt)
        text = response.text.strip()

        # Clean markdown fences
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)

        parsed = json.loads(text)

        # Ensure all fields exist
        parsed.setdefault("title", "")
        parsed.setdefault("company", "")
        parsed.setdefault("location", "")
        parsed.setdefault("min_experience_years", 0)
        parsed.setdefault("required_skills", [])
        parsed.setdefault("preferred_skills", [])
        parsed.setdefault("must_have_requirements", [])
        parsed.setdefault("responsibilities", [])

        return parsed

    def _parse_with_regex(self, jd_text: str) -> dict:
        """Regex-based fallback for JD parsing."""
        # Title
        title_match = re.search(r"JOB TITLE:\s*(.+)", jd_text, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else ""

        # Company
        company_match = re.search(r"COMPANY:\s*(.+)", jd_text, re.IGNORECASE)
        company = company_match.group(1).strip() if company_match else ""

        # Location
        loc_match = re.search(r"LOCATION:\s*(.+)", jd_text, re.IGNORECASE)
        location = loc_match.group(1).strip() if loc_match else ""

        # Experience
        exp_match = re.search(r"(\d+)\+?\s*years?", jd_text, re.IGNORECASE)
        min_exp = int(exp_match.group(1)) if exp_match else 0

        # Required skills
        required_skills = self._extract_section_items(jd_text, "REQUIRED SKILLS")

        # Preferred skills
        preferred_skills = self._extract_section_items(jd_text, "PREFERRED SKILLS")

        # Must-have
        must_have = self._extract_section_items(jd_text, "MUST-HAVE REQUIREMENTS")

        # Responsibilities
        responsibilities = self._extract_section_items(jd_text, "RESPONSIBILITIES")

        return {
            "title": title,
            "company": company,
            "location": location,
            "min_experience_years": min_exp,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "must_have_requirements": must_have,
            "responsibilities": responsibilities,
        }

    def _extract_section_items(self, text: str, section_name: str) -> list[str]:
        """Extract bullet-point items from a named section."""
        pattern = rf"{re.escape(section_name)}\s*\n(.*?)(?=\n\s*(?:[A-Z]{{2,}})|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if not match:
            return []

        items = []
        for line in match.group(1).splitlines():
            line = line.strip().lstrip("•-*● ")
            if line and len(line) > 3:
                items.append(line)
        return items


# ═══════════════════════════════════════════════════════════════
# 2. HYBRID SEARCH ENGINE — Semantic + Keyword
# ═══════════════════════════════════════════════════════════════

class HybridSearchEngine:
    """
    Combines semantic search (ChromaDB embeddings) with keyword matching
    for critical skills to produce better matches.
    """

    def __init__(self, pipeline: ResumeRAGPipeline):
        self.pipeline = pipeline

    def search(self, jd_text: str, parsed_jd: dict, top_k: int = TOP_K) -> list[dict]:
        """
        Hybrid search combining semantic similarity and keyword matching.

        Steps:
        1. Semantic search — embed JD, query ChromaDB for top 2*K candidates
        2. Keyword boost — check exact skill presence in resume text
        3. Merge & re-rank by combined score
        """
        # ── Step 1: Semantic search (cast a wider net) ──
        semantic_results = self.pipeline.search(jd_text, top_k=top_k * 3)

        if not semantic_results:
            return []

        # ── Step 2: Keyword boost for required skills ──
        required_skills = [s.lower() for s in parsed_jd.get("required_skills", [])]
        preferred_skills = [s.lower() for s in parsed_jd.get("preferred_skills", [])]

        # Extract individual skill keywords from multi-word skills
        required_keywords = self._extract_keywords(required_skills)
        preferred_keywords = self._extract_keywords(preferred_skills)

        for result in semantic_results:
            skills_text = result.get("skills", "").lower()
            excerpt_text = result.get("excerpt", "").lower()
            combined_text = skills_text + " " + excerpt_text

            # Count required skill matches
            req_matched = []
            for kw in required_keywords:
                if kw in combined_text:
                    req_matched.append(kw)

            # Count preferred skill matches
            pref_matched = []
            for kw in preferred_keywords:
                if kw in combined_text:
                    pref_matched.append(kw)

            # Calculate keyword score (0 to 1)
            req_score = len(req_matched) / max(len(required_keywords), 1)
            pref_score = len(pref_matched) / max(len(preferred_keywords), 1)
            keyword_score = 0.7 * req_score + 0.3 * pref_score

            result["keyword_score"] = round(keyword_score, 4)
            result["required_skills_matched"] = req_matched
            result["preferred_skills_matched"] = pref_matched

            # ── Step 3: Combined score ──
            # Blend semantic similarity with keyword match
            combined = 0.6 * result["similarity"] + 0.4 * keyword_score
            result["hybrid_score"] = round(combined, 4)

        # Sort by hybrid score and return top K
        semantic_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return semantic_results[:top_k]

    def _extract_keywords(self, skill_phrases: list[str]) -> list[str]:
        """
        Extract individual keywords from skill phrases.
        E.g., "5+ years of professional Python development" → ["python"]
        """
        # Known tech keywords to look for
        tech_keywords = {
            "python", "java", "javascript", "typescript", "go", "golang", "rust",
            "ruby", "scala", "kotlin", "swift", "dart", "c++", "c#",
            "django", "flask", "fastapi", "spring", "react", "next.js", "nextjs",
            "node.js", "nodejs", "express", "nestjs", "rails",
            "postgresql", "mysql", "mongodb", "redis", "cassandra", "elasticsearch",
            "aws", "gcp", "azure", "docker", "kubernetes", "terraform",
            "kafka", "spark", "airflow", "flink", "hadoop",
            "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy",
            "bert", "gpt", "transformer", "nlp", "ml", "ai", "deep learning",
            "graphql", "rest", "grpc", "microservices",
            "jenkins", "github actions", "ci/cd", "git",
            "prometheus", "grafana", "datadog",
            "celery", "rabbitmq", "sqs",
            "flutter", "react native", "swiftui", "jetpack compose",
            "selenium", "playwright", "cypress",
            "solidity", "ethereum", "blockchain",
            "figma", "storybook",
            "snowflake", "bigquery", "redshift", "dbt",
            "mlflow", "sagemaker", "kubeflow",
        }

        keywords = set()
        for phrase in skill_phrases:
            # Direct match against known keywords
            for kw in tech_keywords:
                if kw in phrase:
                    keywords.add(kw)

            # Also extract capitalized words that look like tech terms
            words = re.findall(r"\b[A-Z][a-zA-Z+#.]+\b", phrase)
            for w in words:
                keywords.add(w.lower())

        return list(keywords)


# ═══════════════════════════════════════════════════════════════
# 3. MATCH SCORER — Composite 0-100 scoring
# ═══════════════════════════════════════════════════════════════

class MatchScorer:
    """
    Produces a composite match score (0-100) combining:
    - Semantic similarity (40%)
    - Skill match (30%)
    - Experience match (15%)
    - Education match (15%)
    """

    DEGREE_LEVELS = {
        "phd": 5, "ph.d": 5,
        "mtech": 4, "m.tech": 4, "msc": 4, "m.sc": 4, "mba": 4, "ma": 4, "m.a": 4,
        "btech": 3, "b.tech": 3, "bsc": 3, "b.sc": 3, "bcom": 3, "b.com": 3,
        "bdes": 3, "b.des": 3,
        "diploma": 2,
    }

    def score(self, candidate: dict, parsed_jd: dict) -> dict:
        """
        Score a candidate match (0-100).

        Args:
            candidate: search result dict with similarity, skills, experience_years
            parsed_jd: parsed job description dict

        Returns dict with match_score, breakdown, matched/missing skills, reasoning
        """
        # ── 1. Semantic similarity score (0-100) ──
        semantic_raw = candidate.get("similarity", 0)
        # Scale: 0.3-1.0 similarity → 0-100
        semantic_score = min(100, max(0, (semantic_raw - 0.3) / 0.7 * 100))

        # ── 2. Skill match score (0-100) ──
        required_skills = [s.lower() for s in parsed_jd.get("required_skills", [])]
        preferred_skills = [s.lower() for s in parsed_jd.get("preferred_skills", [])]
        candidate_skills = candidate.get("skills", "").lower()

        matched_required = []
        missing_required = []
        for skill_phrase in required_skills:
            # Check if key terms from the skill phrase appear in candidate's skills
            key_terms = re.findall(r"\b\w{3,}\b", skill_phrase)
            matched = any(term in candidate_skills for term in key_terms)
            if matched:
                matched_required.append(skill_phrase)
            else:
                missing_required.append(skill_phrase)

        matched_preferred = []
        for skill_phrase in preferred_skills:
            key_terms = re.findall(r"\b\w{3,}\b", skill_phrase)
            if any(term in candidate_skills for term in key_terms):
                matched_preferred.append(skill_phrase)

        req_ratio = len(matched_required) / max(len(required_skills), 1)
        pref_ratio = len(matched_preferred) / max(len(preferred_skills), 1)
        skill_score = min(100, (0.7 * req_ratio + 0.3 * pref_ratio) * 100)

        # ── 3. Experience match score (0-100) ──
        candidate_exp = candidate.get("experience_years", 0)
        if isinstance(candidate_exp, str):
            try:
                candidate_exp = int(candidate_exp)
            except (ValueError, TypeError):
                candidate_exp = 0
        required_exp = parsed_jd.get("min_experience_years", 0)

        if required_exp == 0:
            exp_score = 80  # No requirement specified
        elif candidate_exp >= required_exp:
            # Bonus for exceeding, but diminishing returns
            excess = candidate_exp - required_exp
            exp_score = min(100, 80 + excess * 4)
        else:
            # Penalty for under-qualifying
            deficit = required_exp - candidate_exp
            exp_score = max(0, 80 - deficit * 20)

        # ── 4. Education score (0-100) ──
        # Simple heuristic: higher degree = higher score
        edu_score = self._score_education(candidate_skills, parsed_jd)

        # ── Composite score ──
        composite = (
            WEIGHT_SEMANTIC * semantic_score +
            WEIGHT_SKILL * skill_score +
            WEIGHT_EXPERIENCE * exp_score +
            WEIGHT_EDUCATION * edu_score
        )

        return {
            "match_score": round(composite),
            "score_breakdown": {
                "semantic_similarity": round(semantic_score, 1),
                "skill_match": round(skill_score, 1),
                "experience_match": round(exp_score, 1),
                "education_match": round(edu_score, 1),
            },
            "matched_skills": list(set(
                candidate.get("required_skills_matched", []) +
                candidate.get("preferred_skills_matched", [])
            )),
            "missing_skills": missing_required[:5],  # Top 5 gaps
            "candidate_experience_years": candidate_exp,
            "required_experience_years": required_exp,
        }

    def _score_education(self, skills_text: str, parsed_jd: dict) -> int:
        """Score education level (rough heuristic)."""
        # Check for degree mentions in skills/text
        highest = 0
        for degree, level in self.DEGREE_LEVELS.items():
            if degree in skills_text:
                highest = max(highest, level)

        if highest >= 4:
            return 100  # Postgrad
        elif highest >= 3:
            return 75   # Undergrad
        elif highest >= 2:
            return 50   # Diploma
        return 60       # Default (can't determine)


# ═══════════════════════════════════════════════════════════════
# 4. MATCH REASONING — LLM-generated explanations
# ═══════════════════════════════════════════════════════════════

class MatchReasonGenerator:
    """Generate human-readable match explanations using Gemini."""

    def __init__(self):
        self.model = None
        try:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(GEMINI_MODEL)
        except Exception:
            pass

    def generate_reasoning(self, candidate: dict, score_result: dict,
                           parsed_jd: dict) -> str:
        """Generate a concise match reasoning."""
        if self.model:
            try:
                return self._generate_with_llm(candidate, score_result, parsed_jd)
            except Exception as e:
                return self._generate_fallback(candidate, score_result, parsed_jd)

        return self._generate_fallback(candidate, score_result, parsed_jd)

    def _generate_with_llm(self, candidate: dict, score_result: dict,
                           parsed_jd: dict) -> str:
        """Use Gemini to generate reasoning."""
        prompt = f"""Write a concise 2-3 sentence explanation for why this candidate is a match for the job. Be specific about skills and experience.

JOB: {parsed_jd.get('title', 'Unknown')} at {parsed_jd.get('company', 'Unknown')}
Required skills: {', '.join(parsed_jd.get('required_skills', [])[:5])}
Min experience: {parsed_jd.get('min_experience_years', 0)} years

CANDIDATE: {candidate.get('candidate_name', 'Unknown')}
Current role: {candidate.get('current_role', 'Unknown')}
Experience: {candidate.get('experience_years', 0)} years
Matched skills: {', '.join(score_result.get('matched_skills', [])[:8])}
Missing skills: {', '.join(score_result.get('missing_skills', [])[:3])}
Match score: {score_result.get('match_score', 0)}/100
Relevant excerpt: {candidate.get('excerpt', '')[:200]}

Return ONLY the reasoning text, no labels or formatting."""

        response = self.model.generate_content(prompt)
        return response.text.strip()

    def _generate_fallback(self, candidate: dict, score_result: dict,
                           parsed_jd: dict) -> str:
        """Template-based reasoning fallback."""
        name = candidate.get("candidate_name", "Candidate")
        score = score_result.get("match_score", 0)
        matched = score_result.get("matched_skills", [])
        missing = score_result.get("missing_skills", [])
        exp = candidate.get("experience_years", 0)
        role = candidate.get("current_role", "")
        req_exp = parsed_jd.get("min_experience_years", 0)

        parts = []

        # Strength
        if score >= 80:
            parts.append(f"Strong match for {parsed_jd.get('title', 'this role')}.")
        elif score >= 60:
            parts.append(f"Moderate match for {parsed_jd.get('title', 'this role')}.")
        else:
            parts.append(f"Partial match for {parsed_jd.get('title', 'this role')}.")

        # Experience
        if isinstance(exp, str):
            try:
                exp = int(exp)
            except (ValueError, TypeError):
                exp = 0

        if exp >= req_exp:
            parts.append(f"{name} has {exp} years of experience (meets {req_exp}+ year requirement).")
        else:
            parts.append(f"{name} has {exp} years of experience ({req_exp}+ required).")

        # Skills
        if matched:
            parts.append(f"Key matched skills: {', '.join(matched[:5])}.")
        if missing:
            parts.append(f"Gaps: {', '.join(missing[:3])}.")

        return " ".join(parts)


# ═══════════════════════════════════════════════════════════════
# 5. JOB MATCHER — Main orchestrator
# ═══════════════════════════════════════════════════════════════

class JobMatcher:
    """
    End-to-end job matching: JD → parse → hybrid search → score → reason.
    Produces output in the required JSON format.
    """

    def __init__(self):
        print("\nFiring up the Matchmaker...\n")
        self.pipeline = ResumeRAGPipeline()
        self.jd_processor = JobDescriptionProcessor()
        self.search_engine = HybridSearchEngine(self.pipeline)
        self.scorer = MatchScorer()
        self.reasoner = MatchReasonGenerator()
        print()

    def match(self, jd_text: str, jd_file: str = "", top_k: int = TOP_K) -> dict:
        """
        Match a job description against indexed resumes.

        Returns the output in the required format.
        """
        start_time = time.time()

        # ── 1. Parse JD ──
        print(f"  Parsing job description...")
        parsed_jd = self.jd_processor.parse_jd(jd_text)
        print(f"     Title: {parsed_jd['title']}")
        print(f"     Company: {parsed_jd['company']}")
        print(f"     Required skills: {len(parsed_jd['required_skills'])}")
        print(f"     Min experience: {parsed_jd['min_experience_years']}+ years")

        # ── 2. Hybrid search ──
        print(f"\n  Running hybrid search (top {top_k})...")
        candidates = self.search_engine.search(jd_text, parsed_jd, top_k=top_k)

        if not candidates:
            return {
                "job_description": jd_text[:200] + "...",
                "jd_file": jd_file,
                "parsed_jd": parsed_jd,
                "timestamp": datetime.now().isoformat(),
                "top_matches": [],
                "performance_metrics": {
                    "retrieval_latency_ms": round((time.time() - start_time) * 1000),
                    "total_candidates_evaluated": 0,
                    "candidates_after_filter": 0,
                },
            }

        # ── 3. Score & rank ──
        print(f"\n  Scoring {len(candidates)} candidates...")
        scored_matches = []

        for candidate in candidates:
            score_result = self.scorer.score(candidate, parsed_jd)

            # ── 4. Apply must-have filters ──
            if not self._passes_must_have(candidate, parsed_jd):
                score_result["match_score"] = max(0, score_result["match_score"] - 30)
                score_result["filtered_reason"] = "Does not meet must-have requirements"

            scored_matches.append({
                "candidate": candidate,
                "score_result": score_result,
            })

        # Sort by match score
        scored_matches.sort(key=lambda x: x["score_result"]["match_score"], reverse=True)

        # ── 5. Generate reasoning for top matches ──
        print(f"\n  Generating match reasoning...")
        top_matches = []

        for rank, entry in enumerate(scored_matches[:top_k], 1):
            candidate = entry["candidate"]
            score_result = entry["score_result"]

            reasoning = self.reasoner.generate_reasoning(candidate, score_result, parsed_jd)

            match_entry = {
                "rank": rank,
                "candidate_name": candidate.get("candidate_name", "Unknown"),
                "resume_path": f"resumes/{candidate.get('filename', '')}",
                "match_score": score_result["match_score"],
                "score_breakdown": score_result["score_breakdown"],
                "matched_skills": score_result["matched_skills"],
                "missing_skills": score_result["missing_skills"],
                "relevant_excerpts": [candidate.get("excerpt", "")],
                "reasoning": reasoning,
                "experience_years": candidate.get("experience_years", 0),
                "current_role": candidate.get("current_role", ""),
                "location": candidate.get("location", ""),
            }
            top_matches.append(match_entry)

            print(f"     {rank}. {match_entry['candidate_name']} — Score: {match_entry['match_score']}")

        elapsed = time.time() - start_time

        return {
            "job_description": jd_text[:500] + ("..." if len(jd_text) > 500 else ""),
            "jd_file": jd_file,
            "parsed_jd": {
                "title": parsed_jd["title"],
                "company": parsed_jd["company"],
                "min_experience_years": parsed_jd["min_experience_years"],
                "required_skills_count": len(parsed_jd["required_skills"]),
            },
            "timestamp": datetime.now().isoformat(),
            "top_matches": top_matches,
            "performance_metrics": {
                "retrieval_latency_ms": round(elapsed * 1000),
                "total_candidates_evaluated": len(candidates),
                "candidates_after_filter": len(top_matches),
            },
        }

    def _passes_must_have(self, candidate: dict, parsed_jd: dict) -> bool:
        """
        Check if candidate passes must-have requirements.

        Currently checks:
        - Minimum experience years
        """
        min_exp = parsed_jd.get("min_experience_years", 0)
        candidate_exp = candidate.get("experience_years", 0)

        if isinstance(candidate_exp, str):
            try:
                candidate_exp = int(candidate_exp)
            except (ValueError, TypeError):
                candidate_exp = 0

        # Allow 1 year tolerance
        if min_exp > 0 and candidate_exp < min_exp - 1:
            return False

        return True

    def match_file(self, jd_filepath: str, top_k: int = TOP_K) -> dict:
        """Match a JD from a file."""
        print(f"\nLoading JD: {jd_filepath}")

        with open(jd_filepath, "r", encoding="utf-8") as f:
            jd_text = f.read()

        return self.match(jd_text, jd_file=jd_filepath, top_k=top_k)

    def match_all_jds(self, jd_dir: str = str(JD_DIR), output_dir: str = str(OUTPUT_DIR),
                      top_k: int = TOP_K) -> list[dict]:
        """Match all JD files in the directory."""
        os.makedirs(output_dir, exist_ok=True)

        jd_files = sorted([
            f for f in os.listdir(jd_dir)
            if f.endswith(".txt")
        ])

        if not jd_files:
            print(f"No JD files found in {jd_dir}")
            return []

        print(f"\nProcessing {len(jd_files)} job descriptions...\n")
        all_results = []

        for jd_file in jd_files:
            jd_path = os.path.join(jd_dir, jd_file)
            print(f"\n{'='*60}")
            result = self.match_file(jd_path, top_k=top_k)
            all_results.append(result)

            # Save individual result
            output_name = os.path.splitext(jd_file)[0] + "_matches.json"
            output_path = os.path.join(output_dir, output_name)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n  Saved: {output_path}")

        # Save combined results
        combined_path = os.path.join(output_dir, "all_matches.json")
        with open(combined_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\nAll results saved to: {combined_path}")

        return all_results


# ═══════════════════════════════════════════════════════════════
# 6. INTERACTIVE MODE
# ═══════════════════════════════════════════════════════════════

def run_interactive(matcher: JobMatcher):
    """Interactive JD matching mode."""
    print("\n" + "=" * 60)
    print("  Job Matcher — Interactive Mode")
    print("=" * 60)
    print()
    print("  Paste a job description and press Enter twice to match.")
    print("  Type 'quit' to exit.")
    print("-" * 60)

    while True:
        print("\nEnter job description (or 'quit'):\n")
        lines = []
        try:
            while True:
                line = input()
                if line.strip().lower() == "quit":
                    print("\nGoodbye! ")
                    return
                lines.append(line)
                if line.strip() == "" and lines[-2:] == ["", ""]:
                    break
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye! ")
            return

        jd_text = "\n".join(lines).strip()
        if not jd_text:
            continue

        result = matcher.match(jd_text)

        # Display results
        print(f"\n{'='*60}")
        print(f"  Match Results")
        print(f"{'='*60}\n")

        for match in result["top_matches"]:
            print(f"  {match['rank']}. {match['candidate_name']} — Score: {match['match_score']}/100")
            print(f"     Role: {match['current_role']}")
            print(f"     Skills: {', '.join(match['matched_skills'][:5])}")
            print(f"     Reasoning: {match['reasoning']}")
            print()

        metrics = result["performance_metrics"]
        print(f"  Latency: {metrics['retrieval_latency_ms']}ms | "
              f"Evaluated: {metrics['total_candidates_evaluated']}")


# ═══════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Job Matching Engine — Match JDs to indexed resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python job_matcher.py --jd job_descriptions/jd_senior_python_backend.txt
              python job_matcher.py --jd job_descriptions/jd_ml_engineer.txt --top-k 5
              python job_matcher.py --all --output output/
              python job_matcher.py --interactive
        """),
    )
    parser.add_argument("--jd", type=str,
                        help="Path to a job description file")
    parser.add_argument("--all", action="store_true",
                        help="Match all JDs in the job_descriptions/ directory")
    parser.add_argument("--output", type=str, default=str(OUTPUT_DIR),
                        help=f"Output directory for results (default: {OUTPUT_DIR})")
    parser.add_argument("--top-k", type=int, default=TOP_K,
                        help=f"Number of top matches (default: {TOP_K})")
    parser.add_argument("--interactive", action="store_true",
                        help="Run in interactive mode")

    args = parser.parse_args()

    if not any([args.jd, args.all, args.interactive]):
        parser.print_help()
        return

    matcher = JobMatcher()

    if args.jd:
        result = matcher.match_file(args.jd, top_k=args.top_k)

        # Print summary
        print(f"\n{'='*60}")
        print(f"  Match Results for: {result['parsed_jd']['title']}")
        print(f"{'='*60}\n")

        for match in result["top_matches"]:
            print(f"  {match['rank']}. {match['candidate_name']} — Score: {match['match_score']}/100")
            bd = match["score_breakdown"]
            print(f"     Breakdown: Semantic={bd['semantic_similarity']:.0f} | "
                  f"Skill={bd['skill_match']:.0f} | "
                  f"Exp={bd['experience_match']:.0f} | "
                  f"Edu={bd['education_match']:.0f}")
            print(f"     Matched: {', '.join(match['matched_skills'][:5])}")
            if match["missing_skills"]:
                print(f"     Missing: {', '.join(match['missing_skills'][:3])}")
            print(f"     {match['reasoning']}")
            print()

        metrics = result["performance_metrics"]
        print(f"  Latency: {metrics['retrieval_latency_ms']}ms")

        # Save result
        os.makedirs(args.output, exist_ok=True)
        jd_basename = os.path.splitext(os.path.basename(args.jd))[0]
        output_path = os.path.join(args.output, f"{jd_basename}_matches.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"  Full results saved to: {output_path}")

    elif args.all:
        matcher.match_all_jds(output_dir=args.output, top_k=args.top_k)

    elif args.interactive:
        run_interactive(matcher)


if __name__ == "__main__":
    main()
