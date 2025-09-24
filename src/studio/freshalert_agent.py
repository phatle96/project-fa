"""
Fresh Alert Agent - LangGraph Implementation

This module implements a LangGraph-based agent for intelligent food management,
expiration tracking, and recipe recommendations using Fresh Alert and Spoonacular APIs.
"""

from langgraph.graph import StateGraph, END, START
from config.states import MainState
from config.models import get_tools

from config.nodes.conversation import call_model, CONVERSATION
from config.nodes.summarize import summarize_conversation, SUMMARIZE
from config.nodes.log_tool_call import log_tool_calls, LOG_TOOL_CALLS
from config.nodes.async_tool import AsyncToolNode

from config.edges import (
    route_after_summarize,
    route_conversation,
    handle_tool_errors,
)


async def create_graph():
    
    # await get_tools()
    
    workflow = StateGraph(MainState)
    
    # Define a new graph
    workflow = StateGraph(MainState)
    workflow.add_node(CONVERSATION, call_model)
    workflow.add_node(SUMMARIZE, summarize_conversation)
    workflow.add_node("tools", AsyncToolNode(handle_tool_errors=handle_tool_errors))
    workflow.add_node(LOG_TOOL_CALLS, log_tool_calls)

    # Set the entrypoint as conversation
    workflow.add_edge(START, CONVERSATION)

    # conversation -> tools | summarise | __end__
    workflow.add_conditional_edges(
        CONVERSATION,
        route_conversation,
        {"tools": "tools", SUMMARIZE: SUMMARIZE, END: END},
    )

    # summarise -> conversation | __end__
    workflow.add_conditional_edges(
        SUMMARIZE, route_after_summarize, {"tools": "tools", END: END}
    )

    # tools -> log_tool_calls
    workflow.add_edge("tools", LOG_TOOL_CALLS)

    # log_tool_calls -> conversation
    workflow.add_edge(LOG_TOOL_CALLS, CONVERSATION)
    
    
    graph = workflow.compile()
    return graph

async def get_graph():
    """Async graph factory for LangGraph Studio compatibility."""
    return await create_graph()

graph = get_graph()

