"""
MCP tools for Spoonacular API integration.

This module provides tools for the agent to search recipes and get detailed recipe information
using the Spoonacular API through our modular client.
"""

import asyncio
import os
import sys
from typing import List, Optional, Dict, Any, Union
import logging

# Add the src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from utils.spoonacular import (
    SpoonacularClient,
    ComplexSearchRequest,
    Cuisine,
    Diet,
    Intolerance,
    MealType,
    RecipeSort,
    SpoonacularError
)

logger = logging.getLogger(__name__)


class SpoonacularTools:
    """MCP tools for Spoonacular API interactions"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Spoonacular tools
        
        Args:
            api_key: Spoonacular API key (if not provided, will use environment variable)
        """
        self.api_key = api_key or os.getenv("SPOONACULAR_API_KEY")
        if not self.api_key:
            raise ValueError("Spoonacular API key is required. Set SPOONACULAR_API_KEY environment variable or pass api_key parameter.")
    
    async def complex_search_recipes(
        self,
        query: Optional[str] = None,
        cuisine: Optional[Union[str, List[str]]] = None,
        diet: Optional[Union[str, List[str]]] = None,
        intolerances: Optional[Union[str, List[str]]] = None,
        meal_type: Optional[str] = None,
        include_ingredients: Optional[Union[str, List[str]]] = None,
        exclude_ingredients: Optional[Union[str, List[str]]] = None,
        max_ready_time: Optional[int] = None,
        min_ready_time: Optional[int] = None,
        max_calories: Optional[int] = None,
        min_calories: Optional[int] = None,
        max_carbs: Optional[int] = None,
        min_carbs: Optional[int] = None,
        max_protein: Optional[int] = None,
        min_protein: Optional[int] = None,
        max_fat: Optional[int] = None,
        min_fat: Optional[int] = None,
        number: int = 10,
        offset: int = 0,
        sort: Optional[str] = None,
        sort_direction: str = "asc",
        add_recipe_information: bool = True,
        add_recipe_nutrition: bool = False
    ) -> Dict[str, Any]:
        """
        Search for recipes using complex search parameters.
        
        This tool allows searching recipes with advanced filtering including cuisine,
        diet, ingredients, nutritional constraints, and timing requirements.
        
        Args:
            query: Search query (recipe name, keywords)
            cuisine: Cuisine type(s) - can be string or list (e.g., "italian", ["italian", "mexican"])
            diet: Diet type(s) - vegetarian, vegan, gluten free, etc.
            intolerances: Food intolerances - dairy, egg, gluten, etc.
            meal_type: Type of meal - main course, side dish, dessert, etc.
            include_ingredients: Ingredients that must be included
            exclude_ingredients: Ingredients that must not be included
            max_ready_time: Maximum ready time in minutes
            min_ready_time: Minimum ready time in minutes
            max_calories: Maximum calories per serving
            min_calories: Minimum calories per serving
            max_carbs: Maximum carbs in grams
            min_carbs: Minimum carbs in grams
            max_protein: Maximum protein in grams
            min_protein: Minimum protein in grams
            max_fat: Maximum fat in grams
            min_fat: Minimum fat in grams
            number: Number of results to return (1-100)
            offset: Offset for pagination
            sort: Sort criteria (popularity, healthiness, price, time, etc.)
            sort_direction: Sort direction (asc or desc)
            add_recipe_information: Include detailed recipe information
            add_recipe_nutrition: Include nutrition information
            
        Returns:
            Dictionary containing search results with recipes and metadata
            
        Examples:
            # Basic search
            await complex_search_recipes(query="pasta", number=5)
            
            # Advanced search with constraints
            await complex_search_recipes(
                query="chicken curry",
                cuisine=["indian", "thai"],
                diet="gluten free",
                max_ready_time=45,
                min_protein=20,
                number=10
            )
            
            # Ingredient-based search
            await complex_search_recipes(
                include_ingredients=["tomato", "basil"],
                exclude_ingredients=["nuts", "dairy"],
                meal_type="main course"
            )
        """
        try:
            # Convert string parameters to lists if needed
            def to_list(value):
                if value is None:
                    return None
                if isinstance(value, str):
                    return [v.strip() for v in value.split(",")]
                return value
            
            # Convert cuisine strings to enum values
            cuisine_list = None
            if cuisine:
                cuisine_items = to_list(cuisine)
                cuisine_list = []
                for c in cuisine_items:
                    try:
                        cuisine_enum = Cuisine(c.lower().replace(" ", "_"))
                        cuisine_list.append(cuisine_enum)
                    except ValueError:
                        # If enum conversion fails, use string value
                        cuisine_list.append(c)
            
            # Convert diet strings to enum values
            diet_list = None
            if diet:
                diet_items = to_list(diet)
                diet_list = []
                for d in diet_items:
                    try:
                        diet_enum = Diet(d.lower().replace(" ", "_"))
                        diet_list.append(diet_enum)
                    except ValueError:
                        # If enum conversion fails, use string value
                        diet_list.append(d)
            
            # Convert sort string to enum
            sort_enum = None
            if sort:
                try:
                    sort_enum = RecipeSort(sort.lower().replace(" ", "_"))
                except ValueError:
                    # If enum conversion fails, use string value
                    sort_enum = sort
            
            # Create search request
            search_request = ComplexSearchRequest(
                query=query,
                cuisine=cuisine_list,
                diet=diet_list,
                intolerances=to_list(intolerances),
                type=meal_type,
                include_ingredients=to_list(include_ingredients),
                exclude_ingredients=to_list(exclude_ingredients),
                max_ready_time=max_ready_time,
                min_ready_time=min_ready_time,
                max_calories=max_calories,
                min_calories=min_calories,
                max_carbs=max_carbs,
                min_carbs=min_carbs,
                max_protein=max_protein,
                min_protein=min_protein,
                max_fat=max_fat,
                min_fat=min_fat,
                number=min(max(1, number), 100),  # Clamp between 1-100
                offset=max(0, offset),
                sort=sort_enum,
                sort_direction=sort_direction,
                add_recipe_information=add_recipe_information,
                add_recipe_nutrition=add_recipe_nutrition
            )
            
            # Execute search
            async with SpoonacularClient(api_key=self.api_key) as client:
                recipes_api = await client.recipes
                results = await recipes_api.complex_search(search_request)
                
                # Convert to dictionary for MCP response
                response_data = {
                    "total_results": results.total_results,
                    "offset": results.offset,
                    "number": results.number,
                    "recipes": []
                }
                
                for recipe in results.results:
                    recipe_data = {
                        "id": recipe.id,
                        "title": recipe.title,
                        "image": recipe.image,
                        "ready_in_minutes": recipe.ready_in_minutes,
                        "servings": recipe.servings,
                        "source_url": recipe.source_url,
                        "health_score": recipe.health_score,
                        "spoonacular_score": recipe.spoonacular_score,
                        "price_per_serving": recipe.price_per_serving,
                        "cuisines": recipe.cuisines,
                        "dish_types": recipe.dish_types,
                        "diets": recipe.diets,
                        "vegetarian": recipe.vegetarian,
                        "vegan": recipe.vegan,
                        "gluten_free": recipe.gluten_free,
                        "dairy_free": recipe.dairy_free,
                        "very_healthy": recipe.very_healthy,
                        "cheap": recipe.cheap,
                        "very_popular": recipe.very_popular,
                        "sustainable": recipe.sustainable
                    }
                    
                    # Add ingredients if available
                    if recipe.extended_ingredients:
                        recipe_data["ingredients"] = [
                            {
                                "id": ing.id,
                                "name": ing.name,
                                "original": ing.original,
                                "amount": ing.amount,
                                "unit": ing.unit,
                                "aisle": ing.aisle
                            }
                            for ing in recipe.extended_ingredients
                        ]
                    
                    # Add nutrition if available
                    if recipe.nutrition:
                        recipe_data["nutrition"] = {
                            "nutrients": [
                                {
                                    "name": nutrient.name,
                                    "amount": nutrient.amount,
                                    "unit": nutrient.unit
                                }
                                for nutrient in recipe.nutrition.nutrients
                            ]
                        }
                    
                    response_data["recipes"].append(recipe_data)
                
                logger.info(f"Found {results.total_results} recipes for query: {query}")
                return response_data
                
        except SpoonacularError as e:
            logger.error(f"Spoonacular API error in complex search: {e}")
            return {"error": f"Spoonacular API error: {str(e)}", "recipes": []}
        except Exception as e:
            logger.error(f"Unexpected error in complex search: {e}")
            return {"error": f"Unexpected error: {str(e)}", "recipes": []}
    
    async def get_recipe_information(
        self,
        recipe_id: int,
        include_nutrition: bool = True,
        add_wine_pairing: bool = False,
        add_taste_data: bool = False
    ) -> Dict[str, Any]:
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
        try:
            async with SpoonacularClient(api_key=self.api_key) as client:
                recipes_api = await client.recipes
                recipe = await recipes_api.get_recipe_information(
                    recipe_id=recipe_id,
                    include_nutrition=include_nutrition,
                    add_wine_pairing=add_wine_pairing,
                    add_taste_data=add_taste_data
                )
                
                # Convert to dictionary for MCP response
                recipe_data = {
                    "id": recipe.id,
                    "title": recipe.title,
                    "image": recipe.image,
                    "servings": recipe.servings,
                    "ready_in_minutes": recipe.ready_in_minutes,
                    "preparation_minutes": recipe.preparation_minutes,
                    "cooking_minutes": recipe.cooking_minutes,
                    "source_name": recipe.source_name,
                    "source_url": recipe.source_url,
                    "spoonacular_source_url": recipe.spoonacular_source_url,
                    "health_score": recipe.health_score,
                    "spoonacular_score": recipe.spoonacular_score,
                    "price_per_serving": recipe.price_per_serving,
                    "aggregate_likes": recipe.aggregate_likes,
                    "cuisines": recipe.cuisines,
                    "dish_types": recipe.dish_types,
                    "diets": recipe.diets,
                    "occasions": recipe.occasions,
                    "vegetarian": recipe.vegetarian,
                    "vegan": recipe.vegan,
                    "gluten_free": recipe.gluten_free,
                    "dairy_free": recipe.dairy_free,
                    "very_healthy": recipe.very_healthy,
                    "cheap": recipe.cheap,
                    "very_popular": recipe.very_popular,
                    "sustainable": recipe.sustainable,
                    "ketogenic": recipe.ketogenic,
                    "whole30": recipe.whole30,
                    "low_fodmap": recipe.low_fodmap,
                    "weight_watcher_smart_points": recipe.weight_watcher_smart_points,
                    "gaps": recipe.gaps,
                    "instructions": recipe.instructions,
                    "summary": recipe.summary
                }
                
                # Add ingredients
                if recipe.extended_ingredients:
                    recipe_data["ingredients"] = [
                        {
                            "id": ing.id,
                            "name": ing.name,
                            "name_clean": ing.name_clean,
                            "original": ing.original,
                            "original_name": ing.original_name,
                            "amount": ing.amount,
                            "unit": ing.unit,
                            "aisle": ing.aisle,
                            "consistency": ing.consistency,
                            "image": ing.image,
                            "meta": ing.meta
                        }
                        for ing in recipe.extended_ingredients
                    ]
                
                # Add analyzed instructions
                if recipe.analyzed_instructions:
                    recipe_data["analyzed_instructions"] = []
                    for instruction_set in recipe.analyzed_instructions:
                        steps = []
                        for step in instruction_set.steps:
                            step_data = {
                                "number": step.number,
                                "step": step.step,
                                "ingredients": [
                                    {
                                        "id": ing.id,
                                        "name": ing.name,
                                        "image": ing.image
                                    }
                                    for ing in step.ingredients
                                ] if step.ingredients else [],
                                "equipment": [
                                    {
                                        "id": eq.id,
                                        "name": eq.name,
                                        "image": eq.image
                                    }
                                    for eq in step.equipment
                                ] if step.equipment else []
                            }
                            steps.append(step_data)
                        
                        recipe_data["analyzed_instructions"].append({
                            "name": instruction_set.name,
                            "steps": steps
                        })
                
                # Add nutrition information
                if recipe.nutrition and include_nutrition:
                    nutrition_data = {
                        "nutrients": [
                            {
                                "name": nutrient.name,
                                "amount": nutrient.amount,
                                "unit": nutrient.unit,
                                "percent_of_daily_needs": nutrient.percent_of_daily_needs
                            }
                            for nutrient in recipe.nutrition.nutrients
                        ]
                    }
                    
                    if recipe.nutrition.caloric_breakdown:
                        nutrition_data["caloric_breakdown"] = {
                            "percent_protein": recipe.nutrition.caloric_breakdown.percent_protein,
                            "percent_fat": recipe.nutrition.caloric_breakdown.percent_fat,
                            "percent_carbs": recipe.nutrition.caloric_breakdown.percent_carbs
                        }
                    
                    if recipe.nutrition.weight_per_serving:
                        nutrition_data["weight_per_serving"] = {
                            "amount": recipe.nutrition.weight_per_serving.amount,
                            "unit": recipe.nutrition.weight_per_serving.unit
                        }
                    
                    recipe_data["nutrition"] = nutrition_data
                
                # Add wine pairing information
                if recipe.wine_pairing and add_wine_pairing:
                    recipe_data["wine_pairing"] = {
                        "pairing_text": recipe.wine_pairing.pairing_text,
                        "paired_wines": recipe.wine_pairing.paired_wines,
                        "product_matches": [
                            {
                                "id": match.id,
                                "title": match.title,
                                "description": match.description,
                                "price": match.price,
                                "image_url": match.image_url,
                                "average_rating": match.average_rating,
                                "rating_count": match.rating_count,
                                "score": match.score,
                                "link": match.link
                            }
                            for match in recipe.wine_pairing.product_matches
                        ] if recipe.wine_pairing.product_matches else []
                    }
                
                # Add taste information
                if recipe.taste and add_taste_data:
                    recipe_data["taste"] = {
                        "sweetness": recipe.taste.sweetness,
                        "saltiness": recipe.taste.saltiness,
                        "sourness": recipe.taste.sourness,
                        "bitterness": recipe.taste.bitterness,
                        "savoriness": recipe.taste.savoriness,
                        "fattiness": recipe.taste.fattiness,
                        "spiciness": recipe.taste.spiciness
                    }
                
                logger.info(f"Retrieved detailed information for recipe {recipe_id}: {recipe.title}")
                return recipe_data
                
        except SpoonacularError as e:
            logger.error(f"Spoonacular API error getting recipe {recipe_id}: {e}")
            return {"error": f"Spoonacular API error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error getting recipe {recipe_id}: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    async def find_recipes_by_ingredients(
        self,
        ingredients: Union[str, List[str]],
        number: int = 10,
        ranking: int = 1,
        ignore_pantry: bool = True
    ) -> Dict[str, Any]:
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
        try:
            async with SpoonacularClient(api_key=self.api_key) as client:
                logger.info(f"Finding recipes with ingredients: {ingredients}")
                
                recipes_api = await client.recipes
                response = await recipes_api.find_by_ingredients(
                    ingredients=ingredients,
                    number=number,
                    ranking=ranking,
                    ignore_pantry=ignore_pantry
                )
                
                # Convert the response to a more readable format
                recipes_data = []
                for recipe in response.recipes:
                    recipe_data = {
                        "id": recipe.id,
                        "title": recipe.title,
                        "image": recipe.image,
                        "used_ingredient_count": recipe.used_ingredient_count,
                        "missed_ingredient_count": recipe.missed_ingredient_count,
                        "likes": recipe.likes,
                        "used_ingredients": [
                            {
                                "id": ing.id,
                                "name": ing.name,
                                "original": ing.original,
                                "amount": ing.amount,
                                "unit": ing.unit,
                                "aisle": ing.aisle,
                                "image": ing.image,
                                "meta": ing.meta
                            }
                            for ing in recipe.used_ingredients
                        ],
                        "missed_ingredients": [
                            {
                                "id": ing.id,
                                "name": ing.name,
                                "original": ing.original,
                                "amount": ing.amount,
                                "unit": ing.unit,
                                "aisle": ing.aisle,
                                "image": ing.image,
                                "meta": ing.meta
                            }
                            for ing in recipe.missed_ingredients
                        ]
                    }
                    recipes_data.append(recipe_data)
                
                result = {
                    "total_results": len(recipes_data),
                    "recipes": recipes_data
                }
                
                logger.info(f"Found {len(recipes_data)} recipes with provided ingredients")
                return result
                
        except SpoonacularError as e:
            logger.error(f"Spoonacular API error finding recipes by ingredients: {e}")
            return {"error": f"Spoonacular API error: {str(e)}", "recipes": []}
        except Exception as e:
            logger.error(f"Unexpected error finding recipes by ingredients: {e}")
            return {"error": f"Unexpected error: {str(e)}", "recipes": []}


# Global tools instance
_spoonacular_tools = None

def get_spoonacular_tools(api_key: Optional[str] = None) -> SpoonacularTools:
    """Get or create the global Spoonacular tools instance"""
    global _spoonacular_tools
    if _spoonacular_tools is None or api_key:
        _spoonacular_tools = SpoonacularTools(api_key)
    return _spoonacular_tools


# MCP tool functions that can be called by the agent
async def spoonacular_complex_search(
    query: Optional[str] = None,
    cuisine: Optional[Union[str, List[str]]] = None,
    diet: Optional[Union[str, List[str]]] = None,
    intolerances: Optional[Union[str, List[str]]] = None,
    meal_type: Optional[str] = None,
    include_ingredients: Optional[Union[str, List[str]]] = None,
    exclude_ingredients: Optional[Union[str, List[str]]] = None,
    max_ready_time: Optional[int] = None,
    min_ready_time: Optional[int] = None,
    max_calories: Optional[int] = None,
    min_calories: Optional[int] = None,
    max_carbs: Optional[int] = None,
    min_carbs: Optional[int] = None,
    max_protein: Optional[int] = None,
    min_protein: Optional[int] = None,
    max_fat: Optional[int] = None,
    min_fat: Optional[int] = None,
    number: int = 10,
    offset: int = 0,
    sort: Optional[str] = None,
    sort_direction: str = "asc",
    add_recipe_information: bool = True,
    add_recipe_nutrition: bool = False
) -> Dict[str, Any]:
    """
    MCP tool: Search for recipes using complex search parameters.
    
    This is the main tool for finding recipes based on various criteria including
    cuisine, diet, ingredients, nutritional constraints, and timing requirements.
    """
    tools = get_spoonacular_tools()
    return await tools.complex_search_recipes(
        query=query,
        cuisine=cuisine,
        diet=diet,
        intolerances=intolerances,
        meal_type=meal_type,
        include_ingredients=include_ingredients,
        exclude_ingredients=exclude_ingredients,
        max_ready_time=max_ready_time,
        min_ready_time=min_ready_time,
        max_calories=max_calories,
        min_calories=min_calories,
        max_carbs=max_carbs,
        min_carbs=min_carbs,
        max_protein=max_protein,
        min_protein=min_protein,
        max_fat=max_fat,
        min_fat=min_fat,
        number=number,
        offset=offset,
        sort=sort,
        sort_direction=sort_direction,
        add_recipe_information=add_recipe_information,
        add_recipe_nutrition=add_recipe_nutrition
    )


async def spoonacular_get_recipe(
    recipe_id: int,
    include_nutrition: bool = True,
    add_wine_pairing: bool = False,
    add_taste_data: bool = False
) -> Dict[str, Any]:
    """
    MCP tool: Get detailed information about a specific recipe.
    
    This tool retrieves comprehensive information about a recipe including
    ingredients, instructions, nutrition, and optional wine pairing and taste data.
    """
    tools = get_spoonacular_tools()
    return await tools.get_recipe_information(
        recipe_id=recipe_id,
        include_nutrition=include_nutrition,
        add_wine_pairing=add_wine_pairing,
        add_taste_data=add_taste_data
    )


async def spoonacular_find_recipes_by_ingredients(
    ingredients: Union[str, List[str]],
    number: int = 10,
    ranking: int = 1,
    ignore_pantry: bool = True
) -> Dict[str, Any]:
    """
    MCP tool: Find recipes based on available ingredients.
    
    This tool searches for recipes that can be made with the provided ingredients,
    showing which ingredients are used and which additional ingredients are needed.
    Perfect for meal planning with available ingredients or reducing food waste.
    """
    tools = get_spoonacular_tools()
    return await tools.find_recipes_by_ingredients(
        ingredients=ingredients,
        number=number,
        ranking=ranking,
        ignore_pantry=ignore_pantry
    )


# Example usage for testing
if __name__ == "__main__":
    async def test_tools():
        """Test the MCP tools"""
        # Test complex search
        print("🔍 Testing complex search...")
        search_results = await spoonacular_complex_search(
            query="pasta",
            cuisine="italian",
            max_ready_time=30,
            number=3
        )
        
        print(f"Found {search_results['total_results']} recipes")
        for recipe in search_results['recipes'][:2]:
            print(f"- {recipe['title']} (ID: {recipe['id']})")
        
        # Test recipe information
        if search_results['recipes']:
            recipe_id = search_results['recipes'][0]['id']
            print(f"\n📋 Testing recipe information for ID {recipe_id}...")
            
            recipe_info = await spoonacular_get_recipe(
                recipe_id=recipe_id,
                include_nutrition=True,
                add_wine_pairing=True
            )
            
            if 'error' not in recipe_info:
                print(f"Recipe: {recipe_info['title']}")
                print(f"Servings: {recipe_info['servings']}")
                print(f"Ready in: {recipe_info['ready_in_minutes']} minutes")
                if recipe_info.get('nutrition'):
                    nutrients = recipe_info['nutrition']['nutrients']
                    calories = next((n for n in nutrients if n['name'] == 'Calories'), None)
                    if calories:
                        print(f"Calories: {calories['amount']} {calories['unit']}")
    
    # Only run test if SPOONACULAR_API_KEY is set
    if os.getenv("SPOONACULAR_API_KEY"):
        asyncio.run(test_tools())
    else:
        print("Set SPOONACULAR_API_KEY environment variable to test the tools")