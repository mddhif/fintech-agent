

from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

from agents.graph_nodes import ( 
    classify_query, resolve_route, fetch_fintech_banking, fetch_fintech_support, build_response, build_tool_response
)
from .schemas import State, Input, Output
from langgraph.checkpoint.memory import MemorySaver
from agent_mcp.mcp_setup import mcp_tools_node
from langchain_core.tools import tool
from langgraph.prebuilt import tools_condition



@tool
def get_account_balance(account_id: str) -> dict:
    """Fetch current account balance and currency."""
    pass


builder = StateGraph(State, input=Input, output=Output)
builder.add_node("classifier", classify_query)
builder.add_node("fetch_fintech_banking", fetch_fintech_banking)
builder.add_node("fetch_fintech_support", fetch_fintech_support)
builder.add_node("build_response", build_response)
builder.add_node("build_tool_response", build_tool_response)
builder.add_node("tools", mcp_tools_node)
builder.add_node("route_domain", lambda state: state)
builder.add_edge(START, "classifier")
builder.add_conditional_edges(
    "classifier",
    tools_condition,
    {
        "tools": "tools",
        "__end__": "route_domain",
    }
)
builder.add_conditional_edges(
    "route_domain",
    resolve_route
)
builder.add_edge("fetch_fintech_banking", "build_response")
builder.add_edge("fetch_fintech_support", "build_response")

builder.add_edge("build_response", END)

builder.add_edge("tools", "build_tool_response")
builder.add_edge("build_tool_response", END)

graph = builder.compile(checkpointer=MemorySaver())