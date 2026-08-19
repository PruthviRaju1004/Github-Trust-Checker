import hashlib
import uuid

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from .chunker import Chunk

# Deterministic id for the sentinel point that stores a hash of the chunk
# content a collection was built from, so we can tell when a repo's README
# has changed upstream and the cached embeddings need refreshing.
_META_ID = str(uuid.uuid5(uuid.NAMESPACE_URL, "trust-checker/content-hash-meta"))
_META_FILTER = Filter(must_not=[FieldCondition(key="__meta__", match=MatchValue(value=True))])


def _content_hash(chunks: list[Chunk]) -> str:
    joined = "\x1f".join(f"{c.heading}\x1e{c.text}" for c in chunks)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


class QdrantRetriever:
    def __init__(self, chunks, collection_name: str):
        self.chunks = chunks
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = QdrantClient(url="http://localhost:6333")
        self.collection_name = collection_name
        content_hash = _content_hash(chunks)

        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
        else:
            existing = self.client.retrieve(self.collection_name, ids=[_META_ID])
            if existing and existing[0].payload.get("content_hash") == content_hash:
                print(f"Collection '{self.collection_name}' is up to date — skipping re-embedding.")
                return
            print(f"Collection '{self.collection_name}' is stale (README changed) — re-embedding.")
            self.client.delete_collection(self.collection_name)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

        texts = [c.text for c in chunks]
        vectors = self.model.encode(texts)
        points = [
            PointStruct(
                id=i,
                vector=vector.tolist(),
                payload={"heading": chunk.heading, "text": chunk.text},
            )
            for i, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]
        # Sentinel point recording what content this collection was built
        # from, so the next call can detect staleness without re-embedding.
        points.append(
            PointStruct(
                id=_META_ID,
                vector=[0.0] * 384,
                payload={"__meta__": True, "content_hash": content_hash},
            )
        )
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query: str, top_k: int = 3, min_score: float = 0.0):
        query_vector = self.model.encode([query])[0]

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            query_filter=_META_FILTER,
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
