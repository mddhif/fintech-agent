from typing import TypedDict, Annotated, List, Literal, Optional
from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from pydantic import BaseModel
from langchain_core.messages import ToolMessage


class State(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    user_query: str
    domain: Literal["fintech_banking", "fintech_support"]
    documents: list[Document]
    answer: str
    tool_result: str
    tool_message: ToolMessage

class Input(TypedDict):
    user_query: str

class Output(TypedDict):
    documents: list[Document]
    answer: str

class Message(BaseModel):
    role: str
    content: str
    thread_id: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[Message]
