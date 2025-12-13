import os
import logging
from django.core.management.base import BaseCommand
from documents.services.pipeline import process_document
from documents.services.chroma import get_collection

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Process a dataset directory and ingest documents into ChromaDB"

    def add_arguments(self, parser):
        parser.add_argument("dataset_path", type=str)

    def handle(self, *args, **options):
        base_path = options["dataset_path"]
        
        processed = 0
        failed = 0

        for doc_type in os.listdir(base_path):
            type_dir = os.path.join(base_path, doc_type)
            if not os.path.isdir(type_dir):
                continue

            self.stdout.write(f"Processing document type: {doc_type}")

            for filename in os.listdir(type_dir):
                file_path = os.path.join(type_dir, filename)
                if not os.path.isfile(file_path):
                    continue

                try:
                    process_document(file_path, forced_type=doc_type)
                    processed += 1
                    self.stdout.write(f"  ✓ {filename}")
                except Exception as e:
                    failed += 1
                    self.stderr.write(f"  ✗ {filename}: {e}")
                    logger.exception("Failed processing %s", file_path)

        col = get_collection()
        self.stdout.write(f"\nSummary: processed={processed}, failed={failed}")
        self.stdout.write(f"Chroma documents count: {col.count()}")
