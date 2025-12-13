import uuid
import json
from .ocr import ocr_file
from .cleaning import clean_text
from .classify import classify_document
from .extract import extract_entities
from .chroma import get_collection

def process_document(file_path: str, forced_type: str | None = None) -> dict:
    text = clean_text(ocr_file(file_path))

    if forced_type:
        doc_type = forced_type
        confidence = 1.0
    else:
        cls = classify_document(text)
        doc_type = cls["document_type"]
        confidence = cls.get("confidence", 0.0)

    entities = extract_entities(doc_type, text)

    doc_id = str(uuid.uuid4())
    col = get_collection()

    col.upsert(
        ids=[doc_id],
        documents=[text],
        metadatas=[{
            "document_type": doc_type,
            "entities_json": json.dumps(entities, ensure_ascii=False),
            "source_path": str(file_path),
        }],
    )

    return {
        "document_id": doc_id,
        "document_type": doc_type,
        "confidence": confidence,
        "entities": entities,
    }
