
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from unittest.mock import patch

def test_process_document_api_returns_expected_json_structure():
    client = APIClient()

    file = SimpleUploadedFile(
        "invoice.png",
        b"fake-image-bytes",
        content_type="image/png",
    )

    fake_result = {
        "document_id": "test-id",
        "document_type": "invoice",
        "confidence": 0.9,
        "entities": {"invoice_number": "INV-001"},
    }

    with patch("documents.api.process_document", return_value=fake_result):
        resp = client.post("/api/documents/process/", {"file": file}, format="multipart")

    assert resp.status_code == 200
    assert "document_id" in resp.data
    assert "document_type" in resp.data
    assert "confidence" in resp.data
    assert "entities" in resp.data

    assert resp.data["document_type"] == "invoice"
    assert resp.data["entities"]["invoice_number"] == "INV-001"
