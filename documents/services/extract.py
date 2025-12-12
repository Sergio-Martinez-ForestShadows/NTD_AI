from pydantic import BaseModel, Field
from .llm import extract_with_llm

class InvoiceEntities(BaseModel):
    invoice_number: str | None = None
    vendor: str | None = None
    invoice_date: str | None = None
    total: str | None = None
    currency: str | None = None

class GenericEntities(BaseModel):
    entities: dict = Field(default_factory=dict)

def build_prompt(doc_type: str, text: str) -> str:
    return f"""
You are an information extraction system.
Document type: {doc_type}

Extract the relevant entities and return ONLY valid JSON.
Text:
{text}
""".strip()

def extract_entities(doc_type: str, text: str) -> dict:
    # MVP: si no hay LLM configurado, devuelve vacío estructurado
    try:
        raw = extract_with_llm(build_prompt(doc_type, text))
    except Exception:
        return {"entities": {}, "note": "LLM not configured; returning empty entities."}

    # Aquí deberías parsear raw JSON y validarlo con Pydantic según doc_type
    return {"raw": raw}
