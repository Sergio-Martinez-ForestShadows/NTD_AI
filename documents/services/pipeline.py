import uuid
import json
from .ocr import ocr_file
from .cleaning import clean_text
from .classify import classify_document
from .extract import extract_entities
from .chroma import get_collection

def process_document(file_path: str) -> dict:
    text = clean_text(ocr_file(file_path))
    cls = classify_document(text)
    doc_type = cls["document_type"]
    entities = extract_entities(doc_type, text)

    doc_id = str(uuid.uuid4())
    col = get_collection()

    col.upsert(
        ids=[doc_id],
        documents=[text],
        metadatas=[{
            "document_type": doc_type,
            "entities_json": json.dumps(entities, ensure_ascii=False),  # <-- clave
            "source_path": str(file_path),
        }],
    )

    return {
        "document_id": doc_id,
        "document_type": doc_type,
        "confidence": cls.get("confidence", 0.0),
        "entities": entities,
    }
