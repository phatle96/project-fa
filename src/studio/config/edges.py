from langchain_core.messages import HumanMessage
from langgraph.prebuilt import tools_condition
from langgraph.graph import END

from typing_extensions import Literal

from .states import MainState
from .nodes.conversation import CONVERSATION
from .nodes.summarize import SUMMARIZE

def handle_tool_errors(exception):
    """Handle errors from tool execution."""
    error_message = str(exception)
    return HumanMessage(
        content=f"There was an error executing the tool: {error_message}. Please try again with a different approach."
    )


# Determine whether to end or summarize the conversation
def should_summarise(state: MainState) -> Literal[SUMMARIZE, END]:
    """Return the next node to execute."""

    last_summarized_count = state.get("last_summarized_count", 0)
    current_message_count = len(state.get("messages", []))
    
    # Calculate messages since last summary
    messages_since_summary = current_message_count - last_summarized_count
    
    # If there are more than 8 new messages since last summary, then we summarize
    if messages_since_summary >= 8:
        return SUMMARIZE
    
    # Otherwise we can just end
    return END

# Define a function to determine if we should proceed based on authentication status
def check_auth_status(state: MainState) -> Literal["authenticated", "failed"]:
    """Check if authentication was successful."""
    auth_data = state.get("superset_auth")
    if auth_data and auth_data.get("authenticated"):
        return "authenticated"
    return "failed"


def route_conversation(state: MainState) -> Literal["tools", SUMMARIZE, END]:
    """Route conversation based on tool needs and message count."""
    
    # First check if tools are needed
    if tools_condition(state) != END:
        return "tools"
    
    # If no tools needed, check if we should summarize
    return should_summarise(state)


def route_after_summarize(state: MainState) -> Literal["tools", END]:
    """Route after summarization based on the last tool call."""

    # First check if tools are needed
    if tools_condition(state) != END:
        return "tools"
    
    # Otherwise, continue the conversation
    return END
