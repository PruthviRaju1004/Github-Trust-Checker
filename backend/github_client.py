import base64
import requests

def get_readme(owner: str, repo: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "my-trust-checker",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    return content

def parse_repo_url(url: str) -> tuple[str, str]:
    """Turn 'https://github.com/owner/repo' into ('owner', 'repo')."""
    parts = url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo

def get_repo_info(owner: str, repo: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "trust-checker-app"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return {
        "pushed_at": data["pushed_at"],       # last commit date
        "open_issues": data["open_issues_count"],
        "archived": data["archived"],
        "stars": data["stargazers_count"],
    }

# if __name__ == "__main__":
#     owner, repo = "pallets", "flask"
#     info = get_repo_info(owner, repo)
#     print(info)