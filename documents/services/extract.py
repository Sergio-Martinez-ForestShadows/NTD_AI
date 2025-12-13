import re
from datetime import datetime
from .llm import extract_with_llm  # tu capa opcional

INVOICE_NUMBER_RE = re.compile(r"(invoice\s*(number|no\.?)\s*[:#]?\s*)([A-Z0-9\-]+)", re.IGNORECASE)
TOTAL_RE = re.compile(r"(total\s*[:]?[\s$]*)(USD|EUR|COP|MXN|GBP)?\s*([0-9]{1,3}(?:[,\s][0-9]{3})*(?:\.[0-9]{2})?)", re.IGNORECASE)
DATE_RE = re.compile(r"((invoice\s*date|date)\s*[:]?)(\s*[0-9]{4}-[0-9]{2}-[0-9]{2})", re.IGNORECASE)
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)

def _extract_invoice_rules(text: str) -> dict:
    out = {}

    m = INVOICE_NUMBER_RE.search(text)
    if m:
        out["invoice_number"] = m.group(3).strip()

    m = DATE_RE.search(text)
    if m:
        out["invoice_date"] = m.group(3).strip()

    m = TOTAL_RE.search(text)
    if m:
        out["currency"] = (m.group(2) or "").strip() or None
        out["total"] = m.group(3).replace(" ", "").replace(",", "")

    emails = EMAIL_RE.findall(text)
    if emails:
        out["emails"] = sorted(set([e.lower() for e in emails]))

    return out

def extract_entities(doc_type: str, text: str) -> dict:
    doc_type = (doc_type or "unknown").lower().strip()

    # 1) Try LLM if enabled
    llm = extract_with_llm(doc_type, text)
    if llm is not None:
        return llm

    # 2) Fallback rules
    if doc_type == "invoice":
        return _extract_invoice_rules(text)

    # 3) Generic fallback
    return {
        "emails": sorted(set([e.lower() for e in EMAIL_RE.findall(text)])),
        "dates": [m.group(3).strip() for m in DATE_RE.finditer(text)],
    }
