from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .main import handle

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
    answer = handle(request.repo_url, request.message)
    return {"answer": answer}