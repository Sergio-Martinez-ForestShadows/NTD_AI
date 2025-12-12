import os

def extract_with_llm(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "none").lower()
    if provider == "none":
        raise RuntimeError("LLM_PROVIDER=none. Configure LLM_PROVIDER to use an LLM.")
    if provider == "openai":
        # Placeholder: integra el SDK que uses en tu entorno.
        # Mantén aquí la abstracción para que extract.py no dependa del vendor.
        raise NotImplementedError("Implement OpenAI client call here.")
    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")
