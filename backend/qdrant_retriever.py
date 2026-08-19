from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from .chunker import Chunk

class QdrantRetriever:
    def __init__(self, chunks, collection_name: str):
        self.chunks = chunks
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = QdrantClient(url="http://localhost:6333")
        self.collection_name = collection_name
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
        collection_info = self.client.get_collection(self.collection_name)
        already_populated = collection_info.points_count > 0

        if already_populated:
            print(f"Collection '{self.collection_name}' already has data — skipping re-embedding.")
            return
        texts = [c.text for c in chunks]
        vectors = self.model.encode(texts)
        points = []
        for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
            points.append(
                PointStruct(
                    id=i,
                    vector=vector.tolist(),
                    payload={"heading": chunk.heading, "text": chunk.text},
                )
            )
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query: str, top_k: int = 3, min_score: float = 0.0):
        query_vector = self.model.encode([query])[0]

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=top_k,
            score_threshold=min_score if min_score > 0 else None,
        )
        results = []
        for point in response.points:
            chunk = Chunk(heading=point.payload["heading"], text=point.payload["text"])
            results.append((chunk, point.score))
        return results


if __name__ == "__main__":
    from chunker import chunk_markdown

    sample = """# Flask

Flask is lightweight.

## Install

Install with pip: pip install flask

## Quickstart

Run it and go.
"""
    chunks = chunk_markdown(sample)
    retriever = QdrantRetriever(chunks, collection_name="flask_test")
    print("Retriever created, chunks stored.")