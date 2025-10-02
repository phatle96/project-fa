from typing import List, Optional, Dict, Any, Union
from mcp.server.fastmcp import FastMCP
from spoonacular_enum import CUISINE_LIST, MEAL_TYPE_LIST, DIET_LIST
import os, sys

from spoonacular_tools import SpoonacularTools

PORT = 8020

if len(sys.argv) > 1:
    PORT = sys.argv[1]
    
ENV_PORT = os.getenv("SPOONACULAR_MCP_PORT", "")

if ENV_PORT:
    PORT = ENV_PORT
    


mcp = FastMCP("FreshAlertMCP", port=PORT)


mcp = FastMCP("SpoonacularMCP", port=PORT)

tools = SpoonacularTools()

api_key = os.getenv("SPOONACULAR_API_KEY")


@mcp.tool()
async def search_recipes(
    query: Optional[str] = None,
    cuisine: Optional[Union[str, List[str]]] = None,
    diet: Optional[Union[str, List[str]]] = None,
    meal_type: Optional[str] = None,
    number: int = 10,
    offset: int = 0,
    sort_direction: str = "asc",
):
    """
    Search for recipes using complex search parameters.
    
    This tool allows searching recipes with advanced filtering including cuisine,
    diet, ingredients, nutritional constraints, and timing requirements.
    
    Args:
        query: Search query (recipe name, keywords)
        
        cuisine: Cuisine type(s) - can be string or list (e.g., "italian", ["italian", "mexican"]). 
        List of supported cuisine: African, Asian, American, British, Cajun, Caribbean, Chinese, Eastern European, European, French, German, Greek, Indian, Irish, Italian, Japanese, Jewish, Korean, Latin American, Mediterranean, Mexican, Middle Eastern, Nordic, Southern, Spanish, Thai, Vietnamese
        
        diet: Diet type(s) - vegetarian, vegan, gluten free, etc. 
        List of supported diet type: Gluten Free, Ketogenic, Vegetarian, Lacto-Vegetarian, Ovo-Vegetarian, Vegan, Pescetarian, Paleo, Primal, Low FODMAP, Whole30
        
        meal_type: Type of meal - main course, side dish, dessert, etc. 
        List of supported meal type: main course, side dish, dessert, appetizer, salad, bread, breakfast, soup, beverage, sauce, marinade, fingerfood, snack, drink
        
        number: Number of results to return (1-100)
        
        offset: Offset for pagination
        
        sort_direction: Sort direction (asc or desc)
        
    Returns:
        Dictionary containing search results with recipes and metadata
        
    Examples:
        # Basic search
        await search_recipes(query="pasta", number=5)
        
        # Advanced search with constraints
        await search_recipes(
            query="chicken curry",
            cuisine=["indian", "thai"],
            diet="gluten free",
            number=10
        )"""

    return await tools.complex_search_recipes(
        query=query,
        cuisine=cuisine,
        diet=diet,
        meal_type=meal_type,
        number=number,
        offset=offset,
        sort_direction=sort_direction,
    )


@mcp.tool()
async def get_recipe_information(
    recipe_id: int,
    include_nutrition: bool = True,
    add_wine_pairing: bool = False,
    add_taste_data: bool = False,
):
    """
    Get detailed information about a specific recipe.

    This tool retrieves comprehensive information about a recipe including
    ingredients, instructions, nutrition, and optional wine pairing and taste data.

    Args:
        recipe_id: The unique recipe ID from Spoonacular
        include_nutrition: Whether to include detailed nutrition information
        add_wine_pairing: Whether to include wine pairing suggestions
        add_taste_data: Whether to include taste profile information

    Returns:
        Dictionary containing detailed recipe information

    Examples:
        # Basic recipe information
        await get_recipe_information(recipe_id=1096211)

        # Full information with nutrition and wine pairing
        await get_recipe_information(
            recipe_id=1096211,
            include_nutrition=True,
            add_wine_pairing=True,
            add_taste_data=True
        )
    """

    return await tools.get_recipe_information(
        recipe_id=recipe_id,
        include_nutrition=include_nutrition,
        add_wine_pairing=add_wine_pairing,
        add_taste_data=add_taste_data,
    )


@mcp.tool()
async def find_recipes_by_ingredients(
    ingredients: Union[str, List[str]],
    number: int = 10,
    ranking: int = 1,
    ignore_pantry: bool = True,
):
    """
    Find recipes based on available ingredients.

    This tool searches for recipes that can be made with the provided ingredients,
    showing which ingredients are used and which additional ingredients are needed.

    Args:
        ingredients: Ingredients to search with (string or list)
        number: Number of recipes to return (1-100)
        ranking: Ranking optimization (1=maximize used ingredients, 2=minimize missing)
        ignore_pantry: Whether to ignore common pantry items like salt, oil, etc.

    Returns:
        Dictionary containing recipes with ingredient usage information

    Examples:
        # Using string
        await find_recipes_by_ingredients(ingredients="carrots,tomatoes,onions")

        # Using list with optimization to minimize missing ingredients
        await find_recipes_by_ingredients(
            ingredients=["chicken", "rice", "broccoli"],
            ranking=2,
            number=15
        )
    """
    return await tools.find_recipes_by_ingredients(
        ingredients=ingredients,
        number=number,
        ranking=ranking,
        ignore_pantry=ignore_pantry,
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
