import os
import shutil
import pytesseract
from PIL import Image

def ocr_image(image_path: str) -> str:
    tcmd = os.getenv("TESSERACT_CMD")

    if tcmd and os.path.exists(tcmd):
        pytesseract.pytesseract.tesseract_cmd = tcmd
    else:
        # fall back to PATH (Docker installs /usr/bin/tesseract)
        which = shutil.which("tesseract")
        if which:
            pytesseract.pytesseract.tesseract_cmd = which

    return pytesseract.image_to_string(Image.open(image_path))
