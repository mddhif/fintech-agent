

# Fintech AI Agent (LangGraph + MCP + Observability)

This project demonstrates a **Fintech AI Agent backend** built using a **graph-based workflow** capable of:

* Classifying user queries
* Routing requests to domain-specific handlers
* Calling external tools via **Model Context Protocol (MCP)**
* Generating structured responses
* Exposing **metrics and distributed tracing**

The system demonstrates how to build a **production-style AI backend** combining agent orchestration, tool execution, APIs, and observability.

---

# Architecture

The system uses a **graph-based agent workflow** to process user requests.

```
User Request
     │
     ▼
API Endpoint (/chat)
     │
     ▼
Query Classifier
     │
     ├── Tool Required → MCP Tool Execution
     │
     └── Domain Routing
            │
            ├── Banking Service
            └── Support Service
                 │
                 ▼
           Response Builder
                 │
                 ▼
           Final Response
```

The workflow is implemented using **LangGraph**, where nodes represent processing steps and edges represent the execution flow.

---

# Core Components

## API Layer

The service exposes a REST endpoint:

```
POST /api/chat
```

The endpoint:

1. Receives a user query
2. Executes the LangGraph workflow
3. Returns the generated response

Example request:

```json
{
  "content": "What is the balance of account 12345?"
}
```

Example response:

```json
{
  "response": "The available balance for account 12345 is 2450.75 EUR.",
  "thread_id": "generated-thread-id"
}
```

---

# Agent Workflow

The agent workflow consists of several nodes.

| Node                  | Description                                   |
| --------------------- | --------------------------------------------- |
| classifier            | Determines the user intent                    |
| route_domain          | Routes the request to the appropriate handler |
| fetch_fintech_banking | Handles banking-related queries               |
| fetch_fintech_support | Handles support-related queries               |
| tools                 | Executes MCP tools                            |
| build_response        | Builds response from domain services          |
| build_tool_response   | Builds response when a tool was executed      |

Conditional edges allow the system to dynamically decide whether to:

* execute a tool
* route to a domain handler
* generate a direct response

---

# MCP Tool Integration

The agent can call external tools using **Model Context Protocol (MCP)**.

Example capability:

* Fetch account balance
* Retrieve external system data
* Execute backend operations

The MCP tool server runs as a **separate service** and communicates with the agent using **Server-Sent Events (SSE)**.

Tool responses are returned to the agent and incorporated into the final answer.

---

# Observability

The system includes **production-grade observability**.

## Prometheus Metrics

Prometheus metrics are exposed to monitor system activity.

Example metric:

```
fintech_requests_total
```

Metrics endpoint:

```
http://localhost:9464/metrics
```

---

## Distributed Tracing

Tracing is implemented using **OpenTelemetry** and exported via **OTLP**.

Compatible backends include:

* Grafana Tempo
* Jaeger
* OpenTelemetry Collector

Tracing helps visualize:

* agent workflow execution
* tool calls
* latency between processing nodes

---

# Running the Project

## 1 Install Dependencies

```
pip install -r requirements.txt
```

---

## 2 Start the MCP Tool Server

```
python agent_mcp/mcp_sse_server.py
```

Server will run on:

```
http://localhost:8001
```

---

## 3 Start the Fintech Agent API

```
uvicorn main:app --reload
```

Chat endpoint:

```
http://localhost:8000/chat
```

---

# Example Queries

### Banking Query

```
What is my account balance?
```

### Tool-Based Query

```
Check balance of account 12345
```

### Support Query

```
How can I reset my banking password?
```

---

# Technology Stack

* Python
* LangGraph
* FastAPI
* Model Context Protocol (MCP)
* OpenTelemetry
* Prometheus
* Uvicorn





