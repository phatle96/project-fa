import sys
import asyncio

from langchain_core.messages import SystemMessage

from ..states import MainState
from ..prompts import FRESH_ALERT_AGENT_SYSTEM_PROMPT
from ..models import get_tools, get_model


# Define the logic to call the model
async def call_model(state: MainState, config):
    tools = await get_tools(config=config)
    model = get_model(model_config={"provider": "openai", "model_name": "gpt-5-mini"})

    # Get summary if it exists
    summary = state.get("summary", "")

    last_summarized_count = state.get("last_summarized_count", 0)

    system_content = FRESH_ALERT_AGENT_SYSTEM_PROMPT

    # If there is summary, then we add it
    if summary:
        system_content += f"Summary of conversation earlier: {summary}\n\n"

    # Filter and validate message pairs for Anthropic compatibility
    filtered_messages = []
    i = 0
    # Smart message filtering - keep structure but truncate content
    state_messages = state["messages"][last_summarized_count:]

    while i < len(state_messages):
        message = state_messages[i]

        if hasattr(message, "type"):
            if message.type == "human":
                filtered_messages.append(message)
                i += 1
            elif message.type == "ai":
                # Check if this AI message has tool calls
                if hasattr(message, "tool_calls") and message.tool_calls:
                    # Look ahead to see if we have corresponding tool results
                    tool_call_ids = [
                        tc.get("id") for tc in message.tool_calls if tc.get("id")
                    ]

                    # Collect all subsequent tool messages that correspond to these tool calls
                    tool_results = []
                    j = i + 1
                    while j < len(state_messages) and len(tool_results) < len(
                        tool_call_ids
                    ):
                        next_msg = state_messages[j]
                        if (
                            hasattr(next_msg, "type")
                            and next_msg.type == "tool"
                            and hasattr(next_msg, "tool_call_id")
                            and next_msg.tool_call_id in tool_call_ids
                        ):
                            tool_results.append(next_msg)
                        elif hasattr(next_msg, "type") and next_msg.type != "tool":
                            # Stop if we hit a non-tool message
                            break
                        j += 1

                    # Only include the AI message and tool results if we have all corresponding pairs
                    if len(tool_results) == len(tool_call_ids):
                        filtered_messages.append(message)
                        filtered_messages.extend(tool_results)
                        i = j  # Skip past all the tool messages we just processed
                    else:
                        # Skip this AI message and its incomplete tool results
                        while (
                            i + 1 < len(state_messages)
                            and hasattr(state_messages[i + 1], "type")
                            and state_messages[i + 1].type == "tool"
                        ):
                            i += 1
                        i += 1
                else:
                    # AI message without tool calls - safe to include
                    filtered_messages.append(message)
                    i += 1
            elif message.type == "tool":
                # Skip orphaned tool messages (they should have been handled above)
                i += 1
            else:
                # Include other message types
                filtered_messages.append(message)
                i += 1
        else:
            filtered_messages.append(message)
            i += 1

    # Create messages with system message
    messages = [SystemMessage(content=system_content)] + filtered_messages

    # Invoke model with tools
    response = await asyncio.to_thread(
        model.bind_tools(tools).invoke, messages, {"recursion_limit": 125}
    )
    return {"messages": response}


CONVERSATION = sys.intern("conversation")
