from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from main import query_rag

app = FastAPI()

origins = [
    "http://localhost",  # add your frontend root
    "http://localhost/Hacka%20Chat-Bot/front-end",  # full path
    "http://127.0.0.1:8888",  # optional if testing on Live Server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, OPTIONS, GET
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def ask_bot(request: QueryRequest):
    question = request.question.strip()
    if not question:
        return {"answer": "Please type a question."}
    answer = query_rag(question)
    return {"answer": answer}