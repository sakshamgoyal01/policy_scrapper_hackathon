
# 🧠 policy_scrapper – LLM-Powered Query–Retrieval System for Documents

A FastAPI-based intelligent query–retrieval system that processes large policy documents (PDF/DOCX/Email) from insurance, legal, HR, and compliance domains, enabling contextual natural language question answering using LLMs and semantic search.

---

## 🚀 Features

- 📄 Supports PDF, DOCX, and email blob inputs
- 🤖 LLM-powered clause extraction & question answering
- 🔍 Semantic search using FAISS for fast retrieval
- 📚 Clause matching with decision logic evaluation
- 📦 JSON output with clause-level explainability
- 🧠 GPT-4/DeepSeek-based reasoning
- ⚡ Optimized for low latency & token efficiency

---

## 🧱 System Architecture

```mermaid
graph TD
    A[Input: PDF/DOCX/Email Blob] --> B[LLM Parser: Structured Clause Extraction]
    B --> C[Embedding Generation & FAISS Search]
    C --> D[Clause Matching & Context Retrieval]
    D --> E[LLM: Decision Evaluation]
    E --> F[JSON Response Generator]
````

---

## ⚙️ Tech Stack

| Component           | Tech Used               |
| ------------------- | ----------------------- |
| Backend API         | FastAPI                 |
| Embeddings & Search | FAISS                   |
| LLM                 | Groq / GPT-4 / DeepSeek |
| Parser              | PyMuPDF / python-docx   |
| Vector Store        | In-memory FAISS         |
| Deployment          | Render (Free Tier)      |

---

## 📁 Project Structure

```
policy_scrapper/
│
├── main.py                    # FastAPI app entry
├── start.sh                   # Uvicorn start script
├── requirements.txt           # Dependencies
├── render.yaml                # Render deployment config
│
├── routes/
│   └── api.py                 # /hackrx/run endpoint
│
├── services/
│   ├── parser.py              # Extract text from PDFs, DOCX
│   ├── embedding.py           # FAISS indexing & search
│   └── query_eval.py          # LLM-based answer generation
│
├── utils/
│   ├── splitter.py            # Clause segmentation
│   └── formatter.py           # Structured JSON formatting
│
├── models/
│   └── schema.py              # Pydantic models for request/response
│
└── .env                       # (Optional) For local secrets
```

---

## 🧪 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Auth

```
Authorization: Bearer e5f1e25178b58ed57cc1104393ebc3a49b8134fc9b3344b78c47ba0b9d8a9800
```

### 🔄 Endpoint: `/hackrx/run`

**Method:** `POST`
**Content-Type:** `application/json`

#### ✅ Request Body

```json
{
  "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=...",
  "questions": [
    "What is the grace period for premium payment?",
    "Does this policy cover maternity expenses?"
  ]
}
```

#### 📤 Sample Response

```json
{
  "answers": [
    "A grace period of 30 days is provided for premium payment...",
    "Yes, maternity expenses are covered under conditions..."
  ]
}
```

---

## ⚡ Deployment (Render)

### 🔧 Setup Files

#### `start.sh`

```bash
#!/usr/bin/env bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### `render.yaml`

```yaml
services:
  - type: web
    name: policy-scrapper
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: ./start.sh
    branch: main
    region: oregon
    plan: free

---

## 👥 Team

* Built for **HackRx** 2025
* LLM: Groq + DeepSeek 1.3B Instruct
* API built with ❤️ using FastAPI

