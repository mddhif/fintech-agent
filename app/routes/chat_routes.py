from fastapi import FastAPI, APIRouter
from agents.schemas import Message
from agents.fintech_agent import graph
import uuid

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status" : "UP"
    }

thread = {"configurable": {"thread_id": uuid.uuid4()}}
@router.post("/chat")
def chat(body: Message):
    result = graph.invoke({"user_query" : body.content}, thread)
    return {
        "response" : result["answer"]
    }