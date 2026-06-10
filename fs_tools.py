"""
fs_tools.py - File system tools for resume loading.

Copied from Milestone 1 (LLM-Powered File System Assistant) and
used here by resume_rag.py to read PDF, TXT, and DOCX resumes.
"""

import os
import datetime
from typing import Optional


# --- helpers to read different file types ---

def _read_txt(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _read_pdf(filepath):
    from PyPDF2 import PdfReader
    reader = PdfReader(filepath)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


def _read_docx(filepath):
    from docx import Document
    doc = Document(filepath)
    return "\n".join(p.text for p in doc.paragraphs)


# maps extension to the right reader function
_READERS = {
    ".txt": _read_txt,
    ".pdf": _read_pdf,
    ".docx": _read_docx,
}


def read_file(filepath: str) -> dict:
    """
    Reads a resume file and returns its text content + metadata.
    Supports .pdf, .txt and .docx formats.
    """
    try:
        filepath = os.path.abspath(filepath)

        if not os.path.isfile(filepath):
            return {"success": False, "content": None, "metadata": None,
                    "error": f"File not found: {filepath}"}

        ext = os.path.splitext(filepath)[1].lower()
        reader = _READERS.get(ext)
        if reader is None:
            return {"success": False, "content": None, "metadata": None,
                    "error": f"Unsupported format: {ext}. We support: {', '.join(_READERS)}"}

        content = reader(filepath)
        stat = os.stat(filepath)

        metadata = {
            "filename": os.path.basename(filepath),
            "size_bytes": stat.st_size,
            "extension": ext,
            "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }

        return {"success": True, "content": content, "metadata": metadata, "error": None}

    except Exception as e:
        return {"success": False, "content": None, "metadata": None, "error": str(e)}


def list_files(directory: str, extension: Optional[str] = None) -> dict:
    """
    Lists files in a directory. You can optionally filter by extension
    like ".pdf" or ".txt". Returns file metadata for each match.
    """
    try:
        directory = os.path.abspath(directory)

        if not os.path.isdir(directory):
            return {"success": False, "files": [], "total": 0,
                    "error": f"Directory not found: {directory}"}

        if extension and not extension.startswith("."):
            extension = "." + extension

        results = []
        for entry in sorted(os.listdir(directory)):
            full_path = os.path.join(directory, entry)

            if not os.path.isfile(full_path):
                continue

            if extension and not entry.lower().endswith(extension.lower()):
                continue

            stat = os.stat(full_path)
            results.append({
                "name": entry,
                "path": full_path,
                "size_bytes": stat.st_size,
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })

        return {"success": True, "files": results, "total": len(results), "error": None}

    except Exception as e:
        return {"success": False, "files": [], "total": 0, "error": str(e)}
