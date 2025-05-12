import chromadb
import ollama
from chromadb import Documents, EmbeddingFunction, Embeddings

chroma_client = chromadb.Client()


class OllamaEmbeddings(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        response = ollama.embeddings(model="nomic-embed-text", prompt=input)
        return response["embedding"]
