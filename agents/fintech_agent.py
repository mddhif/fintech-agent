

from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

from agents.graph_nodes import ( 
    classify_query, resolve_route, fetch_fintech_banking, fetch_fintech_support, build_response
)
from .schemas import State, Input, Output
from langgraph.checkpoint.memory import MemorySaver




builder = StateGraph(State, input=Input, output=Output)
builder.add_node("classifier", classify_query)
builder.add_node("fetch_fintech_banking", fetch_fintech_banking)
builder.add_node("fetch_fintech_support", fetch_fintech_support)
builder.add_node("build_response", build_response)
builder.add_edge(START, "classifier")
builder.add_conditional_edges("classifier", resolve_route)
builder.add_edge("fetch_fintech_banking", "build_response")
builder.add_edge("fetch_fintech_support", "build_response")
builder.add_edge("build_response", END)

graph = builder.compile(checkpointer=MemorySaver())