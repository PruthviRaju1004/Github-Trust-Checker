from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingRetriever:   
    def __init__(self, chunks):
        self.chunks = chunks
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        texts = [c.text for c in chunks]
        self.vectors = self.model.encode(texts)

    def search(self, query: str, top_k: int = 3, min_score: float = 0.5):
        query_vector = self.model.encode([query])
        scores = cosine_similarity(query_vector, self.vectors)[0]
        ranked = sorted(zip(self.chunks, scores), key=lambda x: x[1], reverse=True)
        filtered = []
        for chunk, score in ranked:
            if score > min_score:
                filtered.append((chunk, score))
        return filtered[:top_k]
        
    
# if __name__ == "__main__":
#     from chunker import chunk_markdown

#     sample = """# Flask

# Flask is lightweight.

# ## Install

# Install with pip: pip install flask

# ## Quickstart

# Run it and go.
# """

#     chunks = chunk_markdown(sample)
#     retriever = EmbeddingRetriever(chunks)

#     query = "how do I install this"
#     results = retriever.search(query, top_k=2)

#     for chunk, score in results:
#         print(f"score={score:.3f} [{chunk.heading}] {chunk.text[:50]!r}")

