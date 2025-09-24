import asyncio, sys

from ..states import MainState


async def log_tool_calls(state: MainState):
    """Log and track tool calls for debugging and state management."""
    messages = state["messages"]
    tool_calls_log = state.get("tool_calls_log", [])
    
    # Find the latest AI message with tool calls
    latest_ai_message = None
    for msg in reversed(messages):
        if hasattr(msg, "type") and msg.type == "ai" and hasattr(msg, "tool_calls") and msg.tool_calls:
            latest_ai_message = msg
            break
    
    if latest_ai_message:
        # Log each tool call
        for tool_call in latest_ai_message.tool_calls:
            log_entry = {
                "timestamp": asyncio.get_event_loop().time(),
                "tool_name": tool_call.get("name"),
                "tool_args": tool_call.get("args"),
                "tool_call_id": tool_call.get("id"),
                "status": "initiated"
            }
            tool_calls_log.append(log_entry)
    
    # Check for tool results and update status
    for msg in reversed(messages):
        if hasattr(msg, "type") and msg.type == "tool":
            # Find corresponding log entry
            for log_entry in reversed(tool_calls_log):
                if log_entry.get("tool_call_id") == msg.tool_call_id:
                    log_entry["status"] = "completed"
                    log_entry["result_preview"] = str(msg.content)[:200] + "..." if len(str(msg.content)) > 200 else str(msg.content)
                    log_entry["completed_at"] = asyncio.get_event_loop().time()
                    break
    
    # Limit the log size to prevent memory issues
    MAX_TOOL_CALLS_LOG = 5  # Keep last 5 tool calls
    if len(tool_calls_log) > MAX_TOOL_CALLS_LOG:
        tool_calls_log = tool_calls_log[-MAX_TOOL_CALLS_LOG:]
    
    return {"tool_calls_log": tool_calls_log}


LOG_TOOL_CALLS = sys.intern("log_tool_calls")