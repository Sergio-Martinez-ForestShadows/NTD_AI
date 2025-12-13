ML Document Classification and Entity Extraction System

Author: Sergio Martinez – Senior Full Stack Developer

Overview

This project implements an end-to-end Document Classification and Entity Extraction System using Django, OCR, vector databases, and machine learning models.

The system processes heterogeneous business documents (invoices, forms, assignments, etc.), identifies their document type using semantic similarity, and extracts structured entities in a scalable and extensible way.

The solution mirrors real-world document intelligence pipelines commonly used in enterprise environments.

Key Capabilities

OCR-based text extraction (Tesseract)

Text cleaning and normalization

Semantic document classification using embeddings

Vector-based similarity search with ChromaDB

Optional LLM-based entity extraction

Rule-based fallback entity extraction (no LLM required)

Django REST API for document processing

Batch dataset ingestion via management command

Fully functional local execution

High-Level Architecture
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
        +--> Entity Extraction
              ├── LLM (optional)
              └── Rule-based fallback (regex)
        |
        v
 Structured JSON Output

Design Decisions

OCR: Tesseract was selected to keep the solution fully local and self-contained.

Vector Database: ChromaDB is used for semantic similarity search and document classification.

Classification: Document type is inferred via nearest-neighbor similarity over embedded document text.

Entity Extraction: Implemented as a pluggable layer:

LLM-based extraction when configured

Rule-based fallback extractors (e.g., invoices) when LLM is disabled

Persistence: ChromaDB persists embeddings and metadata on disk.

Deployment Strategy: Full ML pipeline is intended for local execution due to resource requirements.

Tech Stack

Backend: Python 3.11 / 3.12, Django, Django REST Framework

OCR: Tesseract (via pytesseract)

Vector Database: ChromaDB

Embeddings: Sentence Transformers (all-MiniLM-L6-v2)

LLM (optional): OpenAI or pluggable provider

Testing: pytest, pytest-django

Project Structure
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
│   ├── extract.py      # Entity extraction (LLM + fallback)
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
pytest.ini
.env.example
README.md

Running the Project Locally (After Cloning)

The full document intelligence pipeline is designed to run locally, where sufficient system resources are available to support OCR, embedding models, and vector databases.

1. Clone the Repository
git clone https://github.com/Sergio-Martinez-ForestShadows/NTD_AI.git
cd NTD_AI

2. Create and Activate Virtual Environment

Windows

python -m venv .venv
.\.venv\Scripts\activate


macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

3. Install Python Dependencies
pip install --upgrade pip
pip install -r requirements.txt


Note: This project includes ML and NLP libraries (Torch, Sentence Transformers).
Installation may take several minutes.

4. Install Tesseract OCR

Windows

Download from:
https://github.com/UB-Mannheim/tesseract/wiki

Install to the default location:

C:\Program Files\Tesseract-OCR\


Ensure:

C:\Program Files\Tesseract-OCR\tesseract.exe


macOS

brew install tesseract


Linux (Debian / Ubuntu)

sudo apt-get update
sudo apt-get install -y tesseract-ocr

5. Environment Configuration

Create a .env file at the project root:

DEBUG=true
DJANGO_SECRET_KEY=local-dev-secret
ALLOWED_HOSTS=localhost,127.0.0.1

CHROMA_DIR=.chroma
CHROMA_COLLECTION=documents

TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
LLM_PROVIDER=none
EMBEDDINGS_MODE=local


On macOS / Linux, TESSERACT_CMD can be omitted if Tesseract is in PATH.

6. Initialize Database and Run Server
python manage.py migrate
python manage.py runserver


The API will be available at:

http://localhost:8000/api/documents/process/

Dataset Ingestion (Batch Processing)

A Django management command is provided to ingest datasets:

python manage.py process_dataset dataset


Example output:

Processing document type: invoice
  ✓ invoice_reference.png
Processing document type: form
  ✗ broken_image.jpg: Unsupported file type for OCR MVP: .jpg

Summary: processed=1, failed=1
Chroma documents count: 1


Errors are logged per file

The pipeline continues processing remaining documents

API Usage
Endpoint
POST /api/documents/process/

Request

Content-Type: multipart/form-data

Field: file

Example
curl -X POST http://localhost:8000/api/documents/process/ \
  -F "file=@sample_invoice.png"

Sample Response
{
  "document_id": "21cc7d33-6a39-4ed5-b0e9-9d059d04bc02",
  "document_type": "invoice",
  "confidence": 0.91,
  "entities": {
    "invoice_number": "INV-001",
    "total": "1250.00",
    "currency": "USD",
    "emails": ["billing@acmecorp.com"]
  }
}

Entity Extraction Strategy

LLM-based extraction: Enabled when LLM_PROVIDER is configured.

Rule-based fallback: Included for invoices using regex patterns.

This ensures the system remains functional without external APIs.

Configuration Matrix
Capability	Local Execution	Cloud Containers
OCR (Tesseract)	✅ Supported	⚠️ Resource constrained
Embeddings (Sentence Transformers)	✅ Supported	⚠️ High memory usage
ChromaDB persistence	✅ Local disk	⚠️ Requires persistent disk
LLM extraction	Optional	Optional
Cloud Deployment Note

While the API can be containerized, the full local ML pipeline (OCR + local embeddings + ChromaDB) exceeds the memory limits of lightweight cloud containers.

In real-world production systems, these workloads are typically offloaded to dedicated ML services or external providers.
For this reason, the repository focuses on full local execution, while cloud deployment remains a lightweight demonstration.

Adding New Document Types

Add a new folder to the dataset (e.g., dataset/contract/)

Ingest sample documents using process_dataset

Optionally extend entity extraction logic in extract.py

No database migrations are required.

Testing

Run tests with:

pytest


Tests cover:

Text normalization

Document classification logic

API request/response structure

Conclusion

This project demonstrates a production-oriented approach to document intelligence, combining OCR, semantic search, and optional LLMs within a clean, extensible Django architecture.

The solution prioritizes:

Architectural clarity

Realistic deployment trade-offs

Maintainability and extensibility

Designed and implemented by Sergio Martinez, Senior Full Stack Developer.