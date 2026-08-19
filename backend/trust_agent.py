import os
from datetime import date
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def extract_claims(readme_text: str) -> str:
    prompt = f"""Read the following README and answer these questions based ONLY on what it explicitly claims (not what you know about the project from elsewhere):

1. Does it claim to be actively maintained? (yes/no/not mentioned)
2. Does it claim to be production-ready or stable? (yes/no/not mentioned)
3. Does it mention a specific test coverage percentage? If so, what?

README:
{readme_text}

Answer each question on its own line, briefly."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

def check_trust(readme_text: str, repo_info: dict) -> str:
    claims = extract_claims(readme_text)

    prompt = f"""Here are claims extracted from a project's README:
{claims}

Here is real, live data about the repository:
- Last pushed: {repo_info['pushed_at']}
- Open issues: {repo_info['open_issues']}
- Archived: {repo_info['archived']}
- Stars: {repo_info['stars']}

Today's date is {date.today().isoformat()}.

Compare the claims against the real data. Flag any contradictions clearly (e.g. "README claims X, but the data shows Y"). If nothing contradicts, say so plainly — don't invent a problem that isn't there.

Scope: only compare claims the README actually makes against the data. Do not report on repository health signals (archived status, staleness, issue counts, etc.) that the README never made a claim about — those are out of scope for this check, even if they seem noteworthy. If a claim is "not mentioned," there is nothing to compare it against; do not add supplementary observations about it.

End your response with a final line, exactly in this format, with nothing else on that line:
STATUS: CLEAR
or
STATUS: FLAGGED
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

# if __name__ == "__main__":
#     from github_client import get_readme, parse_repo_url, get_repo_info

#     owner, repo = parse_repo_url("https://github.com/github/accessibilityjs")
#     readme = get_readme(owner, repo)
#     repo_info = get_repo_info(owner, repo)
#     # print(repo_info)
#     info = check_trust(readme, repo_info)
#     # claims = extract_claims(readme)
#     print(info)

    # def parse_repo_url(url: str) -> tuple[str, str]:
    # parts = url.rstrip("/").split("/")
    # owner, repo = parts[-2], parts[-1]
    # if repo.endswith(".git"):
    #     repo = repo[:-4]
    # return owner, repo