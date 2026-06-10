# 🎯 RAG-Based Profile Matching System

Ever had to sift through hundreds of resumes just to find that *one* perfect candidate? It's a massive headache. That's exactly why this project exists. 

This is a complete Retrieval-Augmented Generation (RAG) pipeline designed to do the heavy lifting for you. It reads through resumes (whether they're PDFs, Word docs, or plain text), understands the context, and stores them as vector embeddings in ChromaDB. When you give it a job description, it uses a mix of semantic understanding and keyword matching to find the best candidates, scoring them on a 0–100 scale. 

No more manual screening—just smart, AI-driven matchmaking.

## 🏗️ How It Works

Under the hood, the system is split into two main parts: ingesting the resumes and matching them to jobs. Here's a visual breakdown of the architecture:

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Resumes    │────▶│   Chunker    │────▶│  Embeddings  │
│ (PDF/TXT/    │     │ (Section-    │     │ (HuggingFace │
│  DOCX)       │     │  Aware)      │     │  /OpenAI)    │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                     ┌──────────────┐             ▼
                     │   Metadata   │     ┌──────────────┐
                     │  Extractor   │────▶│   ChromaDB   │
                     │ (Gemini LLM) │     │ Vector Store │
                     └──────────────┘     └──────┬───────┘
                                                  │
┌──────────────┐     ┌──────────────┐             │
│     Job      │────▶│   Hybrid     │◀────────────┘
│ Description  │     │   Search     │
└──────────────┘     │ (Semantic +  │
                     │  Keyword)    │
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐     ┌──────────────┐
                     │   Scorer     │────▶│   Results    │
                     │ (0-100 w/    │     │   (JSON)     │
                     │  breakdown)  │     └──────────────┘
                     └──────────────┘
```

## ✨ What Makes It Cool (Features)

I've broken down the project into two core components:

### 1. The RAG Engine (`resume_rag.py`)
This is where the data ingestion happens.
*   **Reads anything you throw at it:** It can parse PDFs, TXTs, and DOCX files without breaking a sweat.
*   **Smart Chunking:** Instead of blindly cutting text into pieces, it respects the natural structure of a resume (like Skills, Experience, and Education sections).
*   **Flexible Embeddings:** You can use HuggingFace for free, local processing, or plug in OpenAI if you want higher quality.
*   **ChromaDB:** Everything is stored persistently in a local vector database.
*   **LLM Metadata Extraction:** It uses an LLM to smartly pull out names, skills, and experience levels.

### 2. The Matchmaker (`job_matcher.py`)
This is where the magic happens when you're trying to fill a role.
*   **Deep JD Parsing:** It reads job descriptions and figures out exactly what the role actually requires.
*   **Hybrid Search:** It doesn't just look for exact keywords; it understands the *meaning* behind the skills (semantic search) while still making sure critical keywords aren't missed.
*   **Fair Scoring System:** Candidates get a score from 0-100. It's a weighted system (40% semantic, 30% skills, 15% experience, 15% education) so you know *why* someone scored high.
*   **AI Reasoning:** For every match, the LLM actually writes a short explanation of *why* this person is a good fit.
*   **Hard Filters:** It immediately weeds out people who don't meet absolute dealbreakers (like mandatory years of experience).

## 🚀 Getting Started

Want to run this yourself? It's pretty straightforward.

### 1. Set Everything Up

First, clone the project and get your environment ready:

```bash
# Get into the project folder
cd "RAG-Based-Profile-Matching"

# Set up a virtual environment so we don't mess up your global Python
python -m venv venv
venv\Scripts\activate  # If you're on Windows
# source venv/bin/activate # If you're on Mac/Linux

# Install all the necessary packages
pip install -r requirements.txt

# Set up your environment variables
copy .env.example .env
# Open .env and drop in your GEMINI_API_KEY
```

### 2. Generate Some Fake Data
Don't have hundreds of resumes handy? No problem. I've included scripts to generate some realistic fake data to test with:

```bash
# Create 32 diverse sample resumes
python generate_resumes.py

# Create 6 sample job descriptions
python generate_job_descriptions.py
```

### 3. Build the Database
Now we need to process those resumes and get them into ChromaDB:

```bash
# Read all resumes and index them
python resume_rag.py --index

# Curious about what's in the database? Check the stats:
python resume_rag.py --stats

# Want to do a quick manual search?
python resume_rag.py --query "Python Django developer with AWS experience"
```

### 4. Match Candidates to Jobs
Time to find some hires:

```bash
# Match candidates against a specific job description
python job_matcher.py --jd job_descriptions/jd_senior_python_backend.txt

# Or just run it against all job descriptions at once
python job_matcher.py --all --output output/

# Want to step through it interactively?
python job_matcher.py --interactive
```

## 📁 What's Inside?

If you want to dig into the code, here's where everything lives:

```text
RAG Based Profile matching/
├── resume_rag.py                # Part A: The ingestion pipeline
├── job_matcher.py               # Part B: The matching logic
├── config.py                    # Tweak your weights and settings here
├── fs_tools.py                  # Helper functions for reading files
├── generate_resumes.py          # Script to make fake candidates
├── generate_job_descriptions.py # Script to make fake jobs
├── requirements.txt             # Dependencies
├── .env.example                 # Template for your API keys
├── README.md                    # You are here!
├── resumes/                     # Put your candidate files here
├── job_descriptions/            # Put your open roles here
├── chroma_db/                   # The local database lives here
├── output/                      # Where the match results get saved
└── rag_experimentation.ipynb    # A scratchpad notebook for testing
```

## ⚙️ Tweaking the Knobs

Feel free to customize how the system grades candidates. Everything is centralized in `config.py`:

| Setting | Default | What it does |
|---------|---------|--------------|
| `EMBEDDING_PROVIDER` | `huggingface` | Which AI model to use for understanding text. |
| `HF_EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | The specific model from HuggingFace. |
| `CHUNK_MAX_CHARS` | `1500` | How big of a text chunk we feed the AI at once. |
| `TOP_K` | `10` | How many top candidates to return. |
| `WEIGHT_SEMANTIC` | `0.40` | How much we care about general conceptual match. |
| `WEIGHT_SKILL` | `0.30` | How much we care about exact skill matches. |
| `WEIGHT_EXPERIENCE` | `0.15` | How much we weigh their years of experience. |
| `WEIGHT_EDUCATION` | `0.15` | How much we care about their degree. |

## 📊 What Does the Output Look Like?

When the matching is done, you'll get a clean JSON report that looks something like this. Notice how it breaks down the score and actually gives you a plain-English reason for the match!

```json
{
  "job_description": "...",
  "top_matches": [
    {
      "candidate_name": "Arjun Sharma",
      "resume_path": "resumes/resume_arjun_sharma.txt",
      "match_score": 92,
      "score_breakdown": {
        "semantic_similarity": 89.5,
        "skill_match": 95.0,
        "experience_match": 100.0,
        "education_match": 85.0
      },
      "matched_skills": ["Python", "Django", "AWS"],
      "missing_skills": ["Kubernetes"],
      "relevant_excerpts": ["..."],
      "reasoning": "Strong match: 5 years Python/Django experience..."
    }
  ],
  "performance_metrics": {
    "retrieval_latency_ms": 45,
    "total_candidates_evaluated": 30,
    "candidates_after_filter": 10
  }
}
```

## 🔧 The Tech Stack

For the curious developers out there, here's what this is built on:
- **Vector Database**: ChromaDB (because it's lightweight, persistent, and fast)
- **Embeddings**: HuggingFace sentence-transformers (default) or OpenAI
- **LLM Brains**: Google Gemini 1.5 Flash (handles extracting metadata and reasoning out matches)
- **File Parsing**: PyPDF2 and python-docx
- **Language**: Python 3.10+
