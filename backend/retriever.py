from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english")
        texts = [c.text for c in chunks]
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 3):
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]
        ranked = sorted(zip(self.chunks, scores), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
    
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
#     retriever = TfidfRetriever(chunks)

#     query = "how do I install this"
#     results = retriever.search(query, top_k=2)

#     for chunk, score in results:
#         print(f"score={score:.3f} [{chunk.heading}] {chunk.text[:50]!r}")

