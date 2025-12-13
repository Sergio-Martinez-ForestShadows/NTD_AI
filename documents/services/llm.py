import os

def extract_with_llm(doc_type: str, text: str):
    provider = os.getenv("LLM_PROVIDER", "none").lower().strip()
    if provider in ("none", "", "disabled"):
        return None
    # aquí iría OpenAI / HuggingFace; si no lo implementas, lanza NotImplementedError
    raise NotImplementedError("LLM_PROVIDER configured but no provider implementation.")
