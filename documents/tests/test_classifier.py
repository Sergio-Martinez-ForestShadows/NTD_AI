
from unittest.mock import patch
from documents.services.classify import classify_document

def test_classify_document_returns_invoice_when_match_is_good():
    fake_query_result = {
        "ids": [["doc-1"]],
        "metadatas": [[{"document_type": "invoice"}]],
        "distances": [[0.10]], 
    }

    class FakeCollection:
        def query(self, **kwargs):
            return fake_query_result

    with patch("documents.services.classify.get_collection", return_value=FakeCollection()):
        result = classify_document("INVOICE Invoice Number: INV-001", threshold=0.35)

    assert result["document_type"] == "invoice"
    assert result["confidence"] > 0.35
    assert result["matched_id"] == "doc-1"
