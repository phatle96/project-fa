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
    
    # Get image descriptions to replace images in summary
    image_descriptions_map = state.get("image_descriptions", {})

    # Create a narrative summary of the conversation including tool executions
    narrative_messages = []

    for message in new_messages:
        if hasattr(message, "type"):
            if message.type == "human":
                # Check if this message has image descriptions
                message_id = message.id if hasattr(message, 'id') and message.id else str(id(message))
                
                if message_id in image_descriptions_map:
                    # Use the image description instead of the original content
                    narrative_messages.append(f"User: {image_descriptions_map[message_id]}")
                else:
                    # Extract text content, filtering out any images
                    if isinstance(message.content, str):
                        narrative_messages.append(f"User: {message.content}")
                    elif isinstance(message.content, list):
                        text_parts = []
                        for part in message.content:
                            if isinstance(part, dict):
                                # Only include text, skip images
                                if part.get("type") == "text":
                                    text_parts.append(part.get("text", ""))
                            elif isinstance(part, str):
                                text_parts.append(part)
                        if text_parts:
                            narrative_messages.append(f"User: {' '.join(text_parts)}")
            elif message.type == "ai":
                # Handle AI messages with tool calls
                if hasattr(message, "tool_calls") and message.tool_calls:
                    # Summarize tool calls in natural language
                    tool_summaries = []
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.get("name", "unknown_tool")
                        tool_args = tool_call.get("args", {})

                        # Create human-readable summaries for Fresh Alert tools
                        if tool_name == "get_user_products":
                            is_expired = tool_args.get("is_expired")
                            if is_expired == -1:
                                tool_summaries.append("retrieved user's non-expired products")
                            elif is_expired == 1:
                                tool_summaries.append("retrieved user's expired products")
                            elif is_expired == 0:
                                tool_summaries.append("retrieved all user's products (expired and non-expired)")
                            else:
                                tool_summaries.append("retrieved user's food inventory")
                        elif tool_name == "get_expired_products":
                            days = tool_args.get("days", "")
                            if days:
                                tool_summaries.append(f"checked for products expiring in {days} days")
                            else:
                                tool_summaries.append("checked for expired products")
                        elif tool_name == "search_product_code":
                            code = tool_args.get("code", "")[:20]
                            tool_summaries.append(f"searched for product by barcode: {code}")
                        elif tool_name == "create_product_code":
                            product_name = tool_args.get("product_name", "item")
                            tool_summaries.append(f"added new product: {product_name}")
                        elif tool_name == "create_product_date":
                            product_id = tool_args.get("product_id", "")
                            quantity = tool_args.get("quantity", 1)
                            tool_summaries.append(f"added expiration date tracking (quantity: {quantity})")
                        elif tool_name == "search_product_by_name":
                            query = tool_args.get("query", "")[:30]
                            tool_summaries.append(f"searched for product: {query}")
                        elif tool_name == "update_product_date":
                            tool_summaries.append("updated product expiration information")
                        elif tool_name == "delete_product_date":
                            date_ids = tool_args.get("date_ids", [])
                            count = len(date_ids) if isinstance(date_ids, list) else 1
                            if count > 1:
                                tool_summaries.append(f"removed {count} date tracking entries from inventory")
                            else:
                                tool_summaries.append("removed date tracking entry from inventory")
                        elif tool_name == "delete_product":
                            product_ids = tool_args.get("product_ids", [])
                            count = len(product_ids) if isinstance(product_ids, list) else 1
                            if count > 1:
                                tool_summaries.append(f"removed {count} products from inventory")
                            else:
                                tool_summaries.append("removed product from inventory")
                        # Spoonacular recipe tools
                        elif tool_name == "search_recipes":
                            query = tool_args.get("query", "")[:30]
                            if query:
                                tool_summaries.append(f"searched for recipes: {query}")
                            else:
                                tool_summaries.append("searched for recipes")
                        elif tool_name == "get_recipe_information":
                            recipe_id = tool_args.get("recipe_id", "")
                            tool_summaries.append(f"retrieved recipe details")
                        elif tool_name == "find_recipes_by_ingredients":
                            ingredients = tool_args.get("ingredients", [])
                            if isinstance(ingredients, list) and ingredients:
                                ing_str = ", ".join(ingredients[:3])
                                tool_summaries.append(f"found recipes using: {ing_str}")
                            else:
                                tool_summaries.append("found recipes by ingredients")
                        else:
                            # Generic fallback for any other tools
                            tool_summaries.append(f"used {tool_name.replace('_', ' ')}")

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

                        # Fresh Alert tool results
                        if tool_name == "get_user_products":
                            if "total_products" in parsed_content:
                                count = parsed_content["total_products"]
                                narrative_messages.append(f"Found {count} products in inventory")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Error retrieving products: {parsed_content['error']}")
                        elif tool_name == "get_expired_products":
                            if "total_expired" in parsed_content:
                                count = parsed_content["total_expired"]
                                narrative_messages.append(f"Found {count} expired/expiring products")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Error checking expiration: {parsed_content['error']}")
                        elif tool_name == "search_product_code":
                            if "product_name" in parsed_content:
                                name = parsed_content.get("product_name", "Unknown")
                                narrative_messages.append(f"Found product: {name}")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Product not found")
                        elif tool_name == "create_product_code":
                            if "id" in parsed_content or "product" in parsed_content:
                                narrative_messages.append("Product created successfully")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Failed to create product: {parsed_content['error']}")
                        elif tool_name == "create_product_date":
                            if "id" in parsed_content or "success" in parsed_content:
                                narrative_messages.append("Expiration date added successfully")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Failed to add date: {parsed_content['error']}")
                        elif tool_name == "search_product_by_name":
                            if "total_products" in parsed_content:
                                count = parsed_content["total_products"]
                                narrative_messages.append(f"Found {count} matching products")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Search failed: {parsed_content['error']}")
                        elif tool_name == "update_product_date":
                            if "success" in parsed_content or "id" in parsed_content:
                                narrative_messages.append("Product date updated successfully")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Update failed: {parsed_content['error']}")
                        elif tool_name == "delete_product_date":
                            if "success" in parsed_content:
                                deleted_count = parsed_content.get("deleted_count", 1)
                                if deleted_count > 1:
                                    narrative_messages.append(f"{deleted_count} date entries deleted successfully")
                                else:
                                    narrative_messages.append("Date entry deleted successfully")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Date deletion failed: {parsed_content['error']}")
                        elif tool_name == "delete_product":
                            if "success" in parsed_content:
                                deleted_count = parsed_content.get("deleted_count", 1)
                                if deleted_count > 1:
                                    narrative_messages.append(f"{deleted_count} products deleted successfully")
                                else:
                                    narrative_messages.append("Product deleted successfully")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Deletion failed: {parsed_content['error']}")
                        # Spoonacular tool results
                        elif tool_name == "search_recipes":
                            if "total_results" in parsed_content or "results" in parsed_content:
                                results = parsed_content.get("results", [])
                                count = len(results) if isinstance(results, list) else parsed_content.get("total_results", 0)
                                narrative_messages.append(f"Found {count} recipes")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Recipe search failed: {parsed_content['error']}")
                        elif tool_name == "get_recipe_information":
                            if "title" in parsed_content:
                                title = parsed_content.get("title", "")[:50]
                                narrative_messages.append(f"Retrieved recipe: {title}")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Failed to get recipe: {parsed_content['error']}")
                        elif tool_name == "find_recipes_by_ingredients":
                            if isinstance(parsed_content, list):
                                count = len(parsed_content)
                                narrative_messages.append(f"Found {count} recipes matching ingredients")
                            elif "error" in parsed_content:
                                narrative_messages.append(f"Ingredient search failed: {parsed_content['error']}")
                        else:
                            # Generic tool result summary
                            if len(content) > 200:
                                narrative_messages.append(
                                    f"{tool_name.replace('_', ' ')} completed successfully"
                                )
                            else:
                                narrative_messages.append(
                                    f"{tool_name.replace('_', ' ')}: {content[:100]}..."
                                )
                    except (json.JSONDecodeError, AttributeError):
                        # If not JSON or parsing fails, just truncate the content
                        if len(content) > 100:
                            narrative_messages.append(
                                f"{tool_name.replace('_', ' ')} returned data (truncated)"
                            )
                        else:
                            narrative_messages.append(f"{tool_name.replace('_', ' ')}: {content}")

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
    response = await model.ainvoke(input=clean_messages) 

    return {"summary": response.content, "last_summarized_count": messages_count - 2}


SUMMARIZE = sys.intern("summarize_conversation")
