import asyncio
from mcp.client.sse import sse_client
from mcp import ClientSession
from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

async def call_mcp_sse_tool(tool_name, arguments):
    async with sse_client("http://localhost:8001/sse") as (read, write):
         async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                tool_name,
                arguments=arguments
            )

            return result.content[0].text


def mcp_tools_node(state: State) -> State:
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    tool_call_id = tool_call["id"]

    result_text = asyncio.run(call_mcp_sse_tool(tool_name, tool_args))

    return {
        "answer": result_text,
        "messages": ToolMessage(
            content=result_text,
            tool_name=tool_name,
            tool_call_id=tool_call_id

        )
    }
