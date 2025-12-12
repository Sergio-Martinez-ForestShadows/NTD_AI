import os
import shutil
import pytesseract
from PIL import Image

def ocr_image(image_path: str) -> str:
    tcmd = os.getenv("TESSERACT_CMD")

    if tcmd and os.path.exists(tcmd):
        pytesseract.pytesseract.tesseract_cmd = tcmd
    else:
        which = shutil.which("tesseract")
        if which:
            pytesseract.pytesseract.tesseract_cmd = which

    return pytesseract.image_to_string(Image.open(image_path))

def ocr_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"]:
        return ocr_image(file_path)
    raise ValueError(f"Unsupported file type for OCR MVP: {ext}")
