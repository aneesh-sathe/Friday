import os

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from crawler import CrawledResult


def getVectorDB() -> tuple[chromadb.Client, chromadb.Collection]:
    client = chromadb.PersistentClient(
        path=f"{os.getcwd()}", settings=Settings(anonymized_telemetry=False)
    )

    ollama_ef = OllamaEmbeddingFunction(
        url="http://localhost:11434/api/embeddings",
        model_name="nomic-embed-text:latest",
    )

    collection = client.get_or_create_collection(
        name="llm_websearch",
        configuration={
            "hnsw": {
                "space": "cosine",
                "ef_search": 100,
                "ef_construction": 100,
                "max_neighbors": 16,
                "num_threads": 4,
            },
            "embedding_function": ollama_ef,
        },
    )

    return (client, collection)


def addToVectorDB(crawled_result: list[CrawledResult]):
    _, collection = getVectorDB()
    for idx, res in enumerate(crawled_result):
        collection.add(documents=[res.text], metadatas=[{"source": res.url}], ids=[idx])


def get_top_k(query: str):
    pass


getVectorDB()
