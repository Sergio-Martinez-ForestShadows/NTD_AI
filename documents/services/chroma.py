import os
import chromadb
from chromadb.utils import embedding_functions

def get_collection():
    chroma_dir = os.getenv("CHROMA_DIR", ".chroma")
    name = os.getenv("CHROMA_COLLECTION", "documents")

    client = chromadb.PersistentClient(path=chroma_dir)  # :contentReference[oaicite:5]{index=5}
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")  # :contentReference[oaicite:6]{index=6}

    return client.get_or_create_collection(name=name, embedding_function=ef)
