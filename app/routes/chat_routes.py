from fastapi import FastAPI, APIRouter
from agents.schemas import Message
from agents.fintech_agent import graph
import uuid
import logging
import os
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from opentelemetry import trace 
from config.otel_tracing import setup_tracing
import time

router = APIRouter()

langfuse = Langfuse()
callback_handler = CallbackHandler()

#setup_tracing()
#tracer = trace.get_tracer(__name__)

log_path = os.path.expanduser("~/fintech_agent.log")
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

@router.get("/health")
def health_check():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("health-check-span") as span:
        span.set_attribute("test", "ok")
        time.sleep(0.05)
        logging.info("Incoming request --- Health Check")
        return {
            "status" : "UP"
        }

@router.post("/chat")
def chat(body: Message):
    logging.info("Incoming request --- ")
    thread_id = body.thread_id or str(uuid.uuid4())
    logging.info(f"THREAD ID : {thread_id}")
    thread = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke(
        {"user_query" : body.content}, 
        config={
            "run_name": "Fintech Agent -- Chat Endpoint",
            "configurable": {"thread_id": thread_id}, 
            "callbacks": [callback_handler]
            }
        )
    return {
        "response" : result["answer"],
        "thread_id" : thread_id
    }