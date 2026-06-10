"""
config.py - All the Knobs and Dials

This is the centralized configuration for the matching system. 
All the tweakable parameters live here so you can easily adjust things 
like embedding models and scoring weights without diving into the core logic.
"""

import os
from pathlib import Path

# ── Project paths ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
RESUME_DIR = BASE_DIR / "resumes"
JD_DIR = BASE_DIR / "job_descriptions"
OUTPUT_DIR = BASE_DIR / "output"
CHROMA_DB_PATH = str(BASE_DIR / "chroma_db")

# ── Embedding settings ─────────────────────────────────────────
# Supported providers: "huggingface", "openai"
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface")

# HuggingFace (free, runs locally)
HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
HF_EMBEDDING_DIM = 384

# OpenAI (paid API)
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIM = 1536

# ── ChromaDB ───────────────────────────────────────────────────
CHROMA_COLLECTION_NAME = "resumes"

# ── Chunking ───────────────────────────────────────────────────
# Maximum characters per chunk (roughly ~125 tokens per 500 chars)
CHUNK_MAX_CHARS = 1500
# Overlap between chunks when a section is split
CHUNK_OVERLAP_CHARS = 150

# ── Retrieval / matching ───────────────────────────────────────
TOP_K = 10  # number of top matches to return

# Score weights (must sum to 1.0)
WEIGHT_SEMANTIC = 0.40
WEIGHT_SKILL = 0.30
WEIGHT_EXPERIENCE = 0.15
WEIGHT_EDUCATION = 0.15

# ── LLM (Gemini) ──────────────────────────────────────────────
GEMINI_MODEL = "gemini-1.5-flash"

# ── Misc ───────────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}
