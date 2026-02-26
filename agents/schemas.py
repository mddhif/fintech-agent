from typing import TypedDict, Annotated, List, Literal
from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from pydantic import BaseModel


class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str
    domain: Literal["fintech_banking", "fintech_support"]
    documents: list[Document]
    answer: str

class Input(TypedDict):
    user_query: str

class Output(TypedDict):
    documents: list[Document]
    answer: str

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
