from .github_client import get_readme, parse_repo_url, get_repo_info
from .chunker import chunk_markdown
# from retriever import TfidfRetriever
# from .embedding_retriever import EmbeddingRetriever
from .qdrant_retriever import QdrantRetriever
from .qa_agent import ask
from .trust_agent import check_trust
from .router import route
from .build_prompt import contains_injection_attempt

def handle(repo_url: str, message: str) -> str:
    owner, repo = parse_repo_url(repo_url)
    readme = get_readme(owner, repo)
    if contains_injection_attempt(readme):
        return "This repository's README contains content that looks like a prompt injection attempt. Refusing to process it."
    if contains_injection_attempt(message):
        return "Your message contains content that looks like a prompt injection attempt. Please rephrase your question."
    destination = route(message)

    if destination == "qa":
        chunks = chunk_markdown(readme)
        collection_name = f"{owner}_{repo}".replace("-", "_")
        retriever = QdrantRetriever(chunks, collection_name=collection_name)
        results = retriever.search(message, top_k=3, min_score=0.3)
        answer = ask(message, results)
        return answer
    else:
        repo_info = get_repo_info(owner, repo)
        return check_trust(readme, repo_info)
        

if __name__ == "__main__":
    print(handle("https://github.com/pallets/flask", "how do I run a basic flask app"))
    # print(handle("https://github.com/github/accessibilityjs", "is it actively maintained"))