import base64
from urllib.parse import urlparse
import requests


class GitHubError(Exception):
    """Raised when the GitHub API can't fulfill a request (repo not found,
    rate limited, network error, etc). Carries a user-facing message."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def _get_json(url: str, headers: dict) -> dict:
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        raise GitHubError(f"Could not reach GitHub: {e}") from e

    if resp.status_code == 404:
        raise GitHubError("Repository (or its README) was not found on GitHub.", status_code=404)
    if resp.status_code == 403 and resp.headers.get("X-RateLimit-Remaining") == "0":
        raise GitHubError("GitHub API rate limit exceeded. Try again later.", status_code=429)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise GitHubError(f"GitHub API error: {e}", status_code=resp.status_code) from e

    return resp.json()


def get_readme(owner: str, repo: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "my-trust-checker",
    }
    data = _get_json(url, headers)
    content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    return content

def parse_repo_url(url: str) -> tuple[str, str]:
    """Turn 'https://github.com/owner/repo' (optionally with a trailing
    '.git', '/tree/main', query string, etc.) into ('owner', 'repo')."""
    parsed = urlparse(url.strip())
    if parsed.netloc.lower() not in ("github.com", "www.github.com"):
        raise ValueError(f"Not a github.com URL: {url!r}")

    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise ValueError(f"Could not find an owner/repo in URL: {url!r}")

    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo

def get_repo_info(owner: str, repo: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "trust-checker-app"}
    data = _get_json(url, headers)
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