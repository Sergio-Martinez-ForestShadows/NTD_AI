import os
import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import DocumentUploadSerializer
from .services.pipeline import process_document

class ProcessDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        return Response(
            {
                "message": "Use POST multipart/form-data with a 'file' field.",
                "example_curl": "curl -X POST /api/documents/process/ -F \"file=@invoice.jpg\""
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        ser = DocumentUploadSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"errors": ser.errors}, status=status.HTTP_400_BAD_REQUEST)

        f = ser.validated_data["file"]
        suffix = os.path.splitext(f.name)[1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            for chunk in f.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            result = process_document(tmp_path)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass
