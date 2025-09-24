import asyncio

from langchain.agents.tool_node import ToolNode

from ..states import MainState
from config.models import get_tools

class AsyncToolNode:
    def __init__(self, handle_tool_errors=None):
        self.handle_tool_errors = handle_tool_errors

    async def __call__(self, state: MainState, config):
        tools = await get_tools(config=config)
        
        # Track current tool calls before execution
        messages = state["messages"]
        current_tool_calls = []
        
        # Find AI message with tool calls
        for msg in reversed(messages):
            if hasattr(msg, "type") and msg.type == "ai" and hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    current_tool_calls.append({
                        "id": tool_call.get("id"),
                        "name": tool_call.get("name"),
                        "args": tool_call.get("args"),
                        "status": "executing",
                        "started_at": asyncio.get_event_loop().time()
                    })
                break
        
        # Execute tools
        tool_node = ToolNode(tools, handle_tool_errors=self.handle_tool_errors)
        result = await tool_node.ainvoke(state)
        
        # Update tool call status after execution
        for tool_call in current_tool_calls:
            tool_call["status"] = "completed"
            tool_call["completed_at"] = asyncio.get_event_loop().time()
            tool_call["duration"] = tool_call["completed_at"] - tool_call["started_at"]
        
        # Add tracking info to result
        result["current_tool_calls"] = current_tool_calls
        
        return result
