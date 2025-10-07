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
from config.nodes.process_image import PROCESS_IMAGE, process_image_node

from config.edges import (
    route_after_summarize,
    route_conversation,
    handle_tool_errors,
    has_image,
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
    workflow.add_node(PROCESS_IMAGE, process_image_node)

    # Set the entrypoint as conversation
    workflow.add_conditional_edges(
        START, has_image, {True: PROCESS_IMAGE, False: CONVERSATION}
    )

    workflow.add_edge(PROCESS_IMAGE, CONVERSATION)

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


graph = create_graph
