from __future__ import annotations
from .chroma import get_collection

def classify_document(text: str, threshold: float = 0.35, n_results: int = 5) -> dict:
    if not text or not text.strip():
        return {"document_type": "unknown", "confidence": 0.0, "matched_id": None}

    col = get_collection()

    res = col.query(
        query_texts=[text],
        n_results=n_results,
        include=["metadatas", "distances"],
    )

    ids = res.get("ids") or [[]]
    metas = res.get("metadatas") or [[]]
    dists = res.get("distances") or [[]]

    if not ids[0]:
        return {"document_type": "unknown", "confidence": 0.0, "matched_id": None}

    # Pick the first match whose document_type is not 'unknown'
    for i in range(len(ids[0])):
        meta = (metas[0][i] if len(metas[0]) > i else {}) or {}
        doc_type = str(meta.get("document_type", "unknown")).lower().strip()

        dist = dists[0][i] if len(dists[0]) > i else 1.0
        confidence = max(0.0, min(1.0, 1.0 - float(dist)))

        if doc_type != "unknown" and confidence >= threshold:
            return {"document_type": doc_type, "confidence": confidence, "matched_id": ids[0][i]}

    # If everything is unknown or below threshold -> unknown
    return {"document_type": "unknown", "confidence": 0.0, "matched_id": ids[0][0]}
