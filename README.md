1️⃣ README – Nueva sección: Local Execution After Cloning

👉 Copia y pega esta sección en tu README, justo después de Project Structure o antes de Setup Instructions.

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


Note: This project includes ML and NLP libraries (Torch, Sentence Transformers). Installation may take several minutes.

4. Install Tesseract OCR
Windows

Download from:
https://github.com/UB-Mannheim/tesseract/wiki

Install to the default location:

C:\Program Files\Tesseract-OCR\


Ensure tesseract.exe is available at:

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

$ python manage.py process_dataset dataset
Processing document type: invoice
  ✓ invoice_reference.png
Processing document type: form
  ✗ broken_image.jpg: Unsupported file type for OCR MVP: .jpg

Summary: processed=1, failed=1
Chroma documents count: 1

## Configuration Matrix

| Capability | Local (Windows) | Cloud (Render) |
|---|---:|---:|
| OCR (Tesseract) | ✅ Supported | ⚠️ Not deployed (resource limits) |
| Embeddings (Sentence Transformers/ONNX) | ✅ Supported | ⚠️ Heavy memory footprint |
| ChromaDB persistence | ✅ Local disk | ⚠️ Requires persistent disk |
| LLM extraction | Optional | Optional |



On macOS / Linux, TESSERACT_CMD can be omitted if Tesseract is in PATH.

6. Initialize Database and Run Server
python manage.py migrate
python manage.py runserver


The API will be available at:

http://localhost:8000/api/documents/process/

7. Test the API
curl -X POST http://localhost:8000/api/documents/process/ \
  -F "file=@sample_invoice.png"

8. Optional: Dataset Ingestion

To ingest a dataset of documents into ChromaDB:

python manage.py process_dataset <path_to_dataset>

Expected Behavior (Local)

When running locally:

OCR executes using Tesseract

Embeddings are generated via Sentence Transformers

Documents are classified via ChromaDB similarity search

Entity extraction runs through the configured provider

Results are returned as structured JSON

2️⃣ Final Delivery Message (Recruiter / Team)

👉 Este mensaje lo puedes enviar tal cual, solo ajusta el saludo si lo deseas.

Subject: Technical Challenge Submission – ML Document Classification System

Dear Karen Navarro and the NTD team,

I hope you are doing well.

Please find below the delivery of the technical challenge. I would like to provide some context regarding execution and deployment, as this solution intentionally mirrors real-world production constraints.

Solution Summary

This challenge implements a full document intelligence pipeline including:

OCR using Tesseract

Text normalization

Semantic classification using Sentence Transformers + ChromaDB

Pluggable LLM-based entity extraction

Django REST API exposing the processing endpoint

The architecture follows clean separation of concerns and is designed to scale in production environments.

Local vs Cloud Execution

The complete ML pipeline is fully functional when executed locally, where sufficient CPU and memory resources are available to load embedding models and vector databases.

A Dockerized version of the API was deployed to Render for demonstration purposes; however, due to the memory constraints of lightweight cloud containers, ML-heavy components (local embeddings and ChromaDB classification) are intentionally disabled in the cloud deployment.

This reflects a realistic production decision: in enterprise systems, embedding generation and LLM workloads are typically offloaded to dedicated infrastructure or external providers rather than executed inside API containers.

Detailed instructions for local execution after cloning the repository are included in the README.

Repository

Backend (Document Classification System):
https://github.com/Sergio-Martinez-ForestShadows/NTD_AI

Closing Notes

This solution prioritizes:

Architectural clarity

Realistic deployment trade-offs

Production-oriented design decisions

I would be happy to walk through the architecture, explain design choices in more detail, or demonstrate the system locally if needed.

Thank you very much for your time and consideration.

Kind regards,
Sergio Martinez
Senior Full Stack Developer