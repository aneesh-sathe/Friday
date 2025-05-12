import os

import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from crawler import CrawledResult


def getVectorDB() -> tuple[chromadb.Client, chromadb.Collection]:
    client = chromadb.PersistentClient(path=f"{os.getcwd()}")

    ollama_ef = OllamaEmbeddingFunction(
        url="http://localhost:11434/api/embeddings",
        model_name="nomic-embed-text:latest",
    )

    collection = client.get_or_create_collection(
        name="search_embeddings",
        embedding_function=ollama_ef,
        metadata={"hsnw:space": "cosine"},
    )

    return (client, collection)


def addToVectorDB(crawled_result: list[CrawledResult]):
    pass


getVectorDB()
