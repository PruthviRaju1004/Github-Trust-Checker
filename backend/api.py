from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .main import handle
from .github_client import GitHubError

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    repo_url: str
    message: str


@app.get("/")
def root():
    return {"message": "Trust Checker API is running"}


@app.post("/ask")
def ask_endpoint(request: AskRequest):
    try:
        answer = handle(request.repo_url, request.message)
    except ValueError as e:
        # Bad repo_url (not a github.com URL, missing owner/repo, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except GitHubError as e:
        status = e.status_code if e.status_code in (404, 429) else 502
        raise HTTPException(status_code=status, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong while processing that request.")
    return {"answer": answer}