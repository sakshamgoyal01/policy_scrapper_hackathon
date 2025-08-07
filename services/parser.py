import os
import re
import fitz  # PyMuPDF
import requests
from typing import List, Dict


def clean_text(text: str) -> str:
    # Normalize spaces and remove headers/footers if any patterns are consistent
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_clauses_from_text(text: str) -> List[Dict]:
    """
    Extracts clauses using advanced pattern matching and returns structured list.
    Handles hierarchy like 1, 1.1, 1.1.1, etc.
    """
    clause_pattern = re.compile(r"(?m)^(?P<number>(?:\d+\.)*\d+)\s+(?P<text>.+?)(?=^\d+(?:\.\d+)*\s+|\Z)", re.DOTALL)
    matches = clause_pattern.finditer(text)

    clauses = []
    for match in matches:
        number = match.group("number").strip()
        body = match.group("text").strip()
        body = re.sub(r'\s+', ' ', body)
        clauses.append({
            "number": number,
            "text": body
        })
    return clauses


async def load_and_parse_documents(url: str) -> List[Dict]:
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch PDF: {response.status_code}")

    fname = "temp.pdf"
    with open(fname, "wb") as f:
        f.write(response.content)

    doc = fitz.open(fname)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    doc.close()
    os.remove(fname)

    # Clean text and extract clauses
    cleaned_text = clean_text(full_text)
    clauses = extract_clauses_from_text(cleaned_text)

    return clauses
