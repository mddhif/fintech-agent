from .schemas import State
from langchain_core.messages import HumanMessage, SystemMessage
from config.loader import load_prompts
from langchain_openai import ChatOpenAI
from typing import Literal
from .retrieval_setup import fintech_banking_retriever, fintech_support_retriever
from agent_mcp.mcp_sse_server import get_account_balance

tools = [get_account_balance]

classifier_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1).bind_tools(tools)
generator_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompts = load_prompts()

def classify_query(state: State) -> State:
    user_message = HumanMessage(state["user_query"])
    messages = [prompts["classifier_prompt"], *state["messages"], user_message]
    response = classifier_model.invoke(messages)
    return {
        "domain" : response.content,
        "messages" : [user_message, response],
    }


def resolve_route(state: State) -> Literal["fetch_fintech_banking", "fetch_fintech_support"]:
    return "fetch_fintech_banking" if state["domain"] == "fintech_banking" else "fetch_fintech_support"


def fetch_fintech_banking(state: State) -> State:
    documents = fintech_banking_retriever.invoke(state["user_query"])
    return {
        "documents" : documents
    }

def fetch_fintech_support(state: State) -> State:
    documents = fintech_support_retriever.invoke(state["user_query"])
    return {
        "documents" : documents
    }


def build_response(state: State) -> State:
    prompt = (
        prompts["fintech_banking"]["system_prompt"] 
        if state["domain"] == "fintech_banking" 
        else prompts["fintech_support"]["system_prompt"]
    )
    messages = [
        prompt,
        *state["messages"], 
        HumanMessage(f"Documents: {state['documents']}"),
    ]
    response = generator_model.invoke(messages)
    return {
        "answer": response.content,
        "messages": response
    }

