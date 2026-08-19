import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def build_prompt(question: str, chunks: list) -> str:
    context_parts = []
    for chunk, score in chunks:
        context_parts.append(f"--- Source: {chunk.heading} ---\n{chunk.text}")
    context = "\n\n".join(context_parts)
    prompt = f"""You are answering questions using only the text provided below. If the answer isn't in the text, say "I don't have enough information to answer that." After each claim you make, cite which source section it came from, like this: (Source: <heading>).

{context}

Question: {question}"""

    return prompt

def ask(question: str, chunks: list) -> str:
    prompt = build_prompt(question, chunks)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text

# if __name__ == "__main__":
#     from github_client import get_readme, parse_repo_url
#     from chunker import chunk_markdown
#     from embedding_retriever import EmbeddingRetriever

#     owner, repo = parse_repo_url("https://github.com/pallets/flask")
#     readme = get_readme(owner, repo)
#     chunks = chunk_markdown(readme)

#     retriever = EmbeddingRetriever(chunks)
#     question = "how do I run a basic flask app"
#     results = retriever.search(question, top_k=3, min_score=0.3)

#     answer = ask(question, results)
#     print(answer)