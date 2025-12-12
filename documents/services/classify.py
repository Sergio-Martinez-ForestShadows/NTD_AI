from collections import Counter
from .chroma import get_collection

def classify_document(text: str, k: int = 5) -> dict:
    col = get_collection()
    res = col.query(query_texts=[text], n_results=k)

    metas = (res.get("metadatas") or [[]])[0]
    dists = (res.get("distances") or [[]])[0]

    if not metas:
        return {"document_type": "unknown", "confidence": 0.0}

    types = [m.get("document_type", "unknown") for m in metas]
    top_type, count = Counter(types).most_common(1)[0]
    confidence = count / max(len(types), 1)

    return {"document_type": top_type, "confidence": confidence, "neighbors": list(zip(types, dists))}
