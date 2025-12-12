# ML Document Classification and Entity Extraction System

Author: **Sergio Martinez – Senior Full Stack Developer**

---

## Overview

Deployment Note (Cold Start)

Important:
This service is deployed on Render using Docker. When the application has been idle for some time, Render may spin it down.
As a result, the first request can take 30–60 seconds due to container cold start, dependency loading, and OCR initialization.
Subsequent requests are served normally with significantly lower latency.

This project implements an end-to-end **Document Classification and Entity Extraction System** using **Django**, **OCR**, **vector databases**, and **LLMs**. The system is designed to process heterogeneous business documents (invoices, forms, assignments, etc.), identify their document type, and extract structured entities in a scalable and extensible way.

The solution closely mirrors real-world document intelligence pipelines used in enterprise environments.

Endpoint Render Deployed with Docker 
[https://ntd-ai.onrender.com/](https://ntd-ai.onrender.com/)api/

Repository 
[https://github.com/Sergio-Martinez-ForestShadows/NTD_AI](https://github.com/Sergio-Martinez-ForestShadows/NTD_AI)

---

## High-Level Architecture

```
[File Upload / Dataset]
        |
        v
     OCR (Tesseract)
        |
        v
 Text Cleaning & Normalization
        |
        v
 Vector Embedding (Sentence Transformers)
        |
        v
 ChromaDB (Persistent Vector Store)
        |
        +--> Document Type Classification (Similarity Search)
        |
        +--> LLM-based Entity Extraction
        |
        v
 Structured JSON Output
```

### Key Design Decisions

* **OCR**: Tesseract was chosen for local, offline OCR to keep the solution self-contained.
* **Vector DB**: ChromaDB is used for semantic similarity search and document type identification.
* **Classification**: Document type is inferred via nearest-neighbor similarity over embedded document text.
* **Entity Extraction**: LLM-based extraction is abstracted to allow OpenAI or local models.
* **Persistence**: ChromaDB is configured with a persistent disk to survive restarts and redeploys.

---

## Tech Stack

* **Backend**: Python 3.11 / 3.12, Django, Django REST Framework
* **OCR**: Tesseract (via pytesseract)
* **Vector Database**: ChromaDB
* **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
* **LLM (optional)**: OpenAI or pluggable provider
* **Deployment**: Docker + Render
* **Testing**: pytest

---

## Project Structure

```
config/                 # Django project config
├── settings.py
├── urls.py
├── wsgi.py

documents/              # Core application
├── api.py              # REST API views
├── serializers.py
├── urls.py
├── services/
│   ├── ocr.py          # OCR abstraction
│   ├── cleaning.py     # Text normalization
│   ├── chroma.py       # ChromaDB client
│   ├── classify.py     # Document classification logic
│   ├── llm.py          # LLM abstraction layer
│   ├── extract.py      # Entity extraction
│   └── pipeline.py     # End-to-end processing pipeline
├── management/
│   └── commands/
│       └── process_dataset.py
├── tests/
│   ├── test_cleaning.py
│   ├── test_classifier.py
│   └── test_api.py

Dockerfile
requirements.txt
.env.example
README.md
```

---

## Setup Instructions (Local – Windows)

### 1. Prerequisites

* Python 3.11+
* Tesseract OCR installed and available in PATH
* Git

### 2. Environment Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
CHROMA_DIR=.chroma
CHROMA_COLLECTION=documents
TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
LLM_PROVIDER=none
OPENAI_API_KEY=
```

### 3. Run Migrations and Server

```bash
python manage.py migrate
python manage.py runserver
```

---

## Batch Processing (Dataset Ingestion)

A Django management command is provided to process a dataset directory:

```bash
python manage.py process_dataset <path_to_dataset>
```

This command:

* Iterates over supported document files
* Extracts text via OCR
* Classifies document type
* Extracts entities
* Upserts results into ChromaDB
* Logs failures without stopping the pipeline

---

## API Usage

### Endpoint

`POST /api/documents/process/`

### Request

* Content-Type: `multipart/form-data`
* Field: `file`

### Example (curl)

```bash
curl -X POST http://localhost:8000/api/documents/process/ \
  -F "file=@invoice.png"
```

### Response Example

```json
{
  "document_id": "0437edc3-cc8b-46c0-a746-30e4a53ccc1a",
  "document_type": "invoice",
  "confidence": 0.87,
  "entities": {
    "invoice_number": "INV-001",
    "vendor": "ACME Corp",
    "total": "1250.00",
    "currency": "USD"
  }
}
```

---

## Deployment on Render (Docker)

This project is designed to be deployed on **Render using Docker**, which allows system-level dependencies such as Tesseract.

### Key Environment Variables

```env
CHROMA_DIR=/var/data/chroma
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

A **Persistent Disk** must be attached and mounted to `/var/data` to preserve ChromaDB data across deploys.

---

## Adding New Document Types

1. Define entity schema in `extract.py`
2. Update LLM prompt logic for the new type
3. Ingest sample documents via `process_dataset`
4. ChromaDB will automatically start classifying against the new type

No schema or migration changes are required.

---

## Testing

Run tests with:

```bash
pytest
```

Tests cover:

* Text cleaning
* Document classification logic
* API upload and response structure

---

## Known Limitations

* MVP OCR supports images only (PDF support can be added via Poppler or cloud OCR)
* Entity extraction requires LLM configuration
* Classification accuracy improves as more documents are ingested

---

## Conclusion

This solution demonstrates a production-oriented approach to document intelligence, combining OCR, semantic search, and LLMs within a clean, extensible Django architecture.

Designed and implemented by **Sergio Martinez**, Senior Full Stack Developer.
