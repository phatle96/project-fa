"""
Summarization node for the Fresh Alert Agent.

This module handles conversation summarization to manage context length
and maintain conversation coherence over long interactions.
"""

import asyncio
import sys

from langchain_core.messages import HumanMessage

from ..states import MainState
from ..models import get_model


SUMMARIZATION_PROMPT = """Please summarize this conversation between a user and a Fresh Alert Agent.

The Fresh Alert Agent helps users manage their food inventory, track expiration dates, and find recipes.

Focus on:
1. Key information about the user's food inventory
2. Any expiring or expired products discussed
3. Recipe suggestions or meal planning discussed
4. User preferences or dietary needs mentioned
5. Any ongoing tasks or follow-ups needed

Keep the summary concise but include important details about food items, dates, and user preferences.
"""


async def summarize_conversation(state: MainState):
    model = get_model(model_config={"provider": "openai", "model_name": "gpt-5-mini"})

    # First, we get any existing summary
    summary = state.get("summary", "")

    # Get messages that haven't been summarized yet
    # Use a marker or count to track what's been summarized
    messages_count = len(state["messages"])
    last_summarized_count = state.get("last_summarized_count", 0)

    # Only summarize new messages since last summary
    new_messages = state["messages"][last_summarized_count:]

    # Create a narrative summary of the conversation including tool executions
    narrative_messages = []

    for message in new_messages:
        if hasattr(message, "type"):
            if message.type == "human":
                narrative_messages.append(f"User: {message.content}")
            elif message.type == "ai":
                # Handle AI messages with tool calls
                if hasattr(message, "tool_calls") and message.tool_calls:
                    # Summarize tool calls in natural language
                    tool_summaries = []
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.get("name", "unknown_tool")
                        tool_args = tool_call.get("args", {})

                        # Create human-readable summaries for common tools
                        if tool_name == "superset_sqllab_execute_query":
                            sql = (
                                tool_args.get("sql", "")[:100] + "..."
                                if len(tool_args.get("sql", "")) > 100
                                else tool_args.get("sql", "")
                            )
                            tool_summaries.append(f"executed SQL query: {sql}")
                        elif tool_name == "superset_explore_permalink_create":
                            viz_type = tool_args.get("form_data", {}).get(
                                "viz_type", "unknown"
                            )
                            tool_summaries.append(f"created a {viz_type} chart")
                        elif tool_name.startswith("superset_"):
                            tool_summaries.append(
                                f"used {tool_name.replace('superset_', '').replace('_', ' ')}"
                            )
                        else:
                            tool_summaries.append(f"used {tool_name}")

                    if tool_summaries:
                        narrative_messages.append(
                            f"Assistant: {', '.join(tool_summaries)}"
                        )

                # Also include any text content from AI messages
                if hasattr(message, "content") and message.content:
                    if isinstance(message.content, str):
                        narrative_messages.append(f"Assistant: {message.content}")
                    elif isinstance(message.content, list):
                        text_parts = []
                        for part in message.content:
                            if isinstance(part, dict) and part.get("type") == "text":
                                text_parts.append(part.get("text", ""))
                        if text_parts:
                            narrative_messages.append(
                                f"Assistant: {' '.join(text_parts)}"
                            )

            elif message.type == "tool":
                # Summarize tool results in natural language
                tool_name = getattr(message, "name", "unknown_tool")
                content = message.content

                # Try to extract meaningful information from tool results
                if isinstance(content, str):
                    try:
                        import json

                        parsed_content = json.loads(content)

                        if tool_name == "superset_sqllab_execute_query":
                            if "data" in parsed_content:
                                row_count = len(parsed_content["data"])
                                narrative_messages.append(
                                    f"Query returned {row_count} rows of data"
                                )
                            elif "error" in parsed_content:
                                narrative_messages.append(
                                    f"Query failed: {parsed_content['error']}"
                                )
                        elif tool_name == "superset_explore_permalink_create":
                            if "url" in parsed_content:
                                narrative_messages.append(f"Chart created successfully")
                            elif "error" in parsed_content:
                                narrative_messages.append(
                                    f"Chart creation failed: {parsed_content['error']}"
                                )
                        else:
                            # Generic tool result summary
                            if len(content) > 200:
                                narrative_messages.append(
                                    f"{tool_name} returned data (truncated)"
                                )
                            else:
                                narrative_messages.append(
                                    f"{tool_name} returned: {content[:100]}..."
                                )
                    except (json.JSONDecodeError, AttributeError):
                        # If not JSON or parsing fails, just truncate the content
                        if len(content) > 100:
                            narrative_messages.append(
                                f"{tool_name} returned data (truncated)"
                            )
                        else:
                            narrative_messages.append(f"{tool_name}: {content}")

    # Convert narrative to clean messages for summarization
    conversation_text = "\n".join(narrative_messages)

    # Create our summarization prompt
    if summary:
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            f"Recent conversation:\n{conversation_text}\n\n"
            "Extend the summary by taking into account the new messages above"
        )
    else:
        summary_message = (
            f"{SUMMARIZATION_PROMPT}\n"
            f"Recent conversation:\n{conversation_text}\n\n"
        )

    # Create clean messages for the model (no tool calls)
    clean_messages = [HumanMessage(content=summary_message)]

    # Use model without tools to avoid any tool-related issues
    response = await asyncio.to_thread(model.invoke, clean_messages)

    # Delete all but the 2 most recent messages
    # delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "last_summarized_count": messages_count - 2}


SUMMARIZE = sys.intern("summarize_conversation")
