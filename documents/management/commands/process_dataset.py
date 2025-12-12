import os
import glob
import logging
from django.core.management.base import BaseCommand
from documents.services.pipeline import process_document

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Process a dataset directory and upsert documents into ChromaDB."

    def add_arguments(self, parser):
        parser.add_argument("dataset_path", type=str)

    def handle(self, *args, **opts):
        dataset_path = opts["dataset_path"]
        files = []
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.tif", "*.tiff", "*.bmp"):
            files.extend(glob.glob(os.path.join(dataset_path, "**", ext), recursive=True))

        self.stdout.write(f"Found {len(files)} files under {dataset_path}")

        ok, fail = 0, 0
        for fp in files:
            try:
                out = process_document(fp)
                ok += 1
                self.stdout.write(f"OK: {fp} -> {out['document_type']}")
            except Exception as e:
                fail += 1
                logger.exception("Failed processing %s", fp)
                self.stderr.write(f"FAIL: {fp} ({e})")

        self.stdout.write(f"Done. ok={ok} fail={fail}")
