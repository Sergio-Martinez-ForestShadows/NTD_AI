import os
import json
import chromadb

def get_collection():
    client = chromadb.PersistentClient(path=os.getenv("CHROMA_DIR", ".chroma"))
    return client.get_or_create_collection(name=os.getenv("CHROMA_COLLECTION", "documents"))

def upsert_document(collection, doc_id: str, text: str, doc_type: str, confidence: float, entities: dict):
    metadata = {
        "document_type": str(doc_type),
        "confidence": float(confidence),
        # store as JSON string (metadata must be primitive types)
        "entities_json": json.dumps(entities, ensure_ascii=False),
    }

    collection.upsert(
        ids=[doc_id],
        documents=[text],
        metadatas=[metadata],
    )
