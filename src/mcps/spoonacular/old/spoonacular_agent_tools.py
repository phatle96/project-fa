"""
Simple agent tools for Spoonacular API.

This module provides easy-to-use functions that can be called directly by agents
for recipe search and information retrieval.
"""

import os
import sys
import asyncio
from typing import List, Optional, Dict, Any, Union

# Add the src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from utils.spoonacular import SpoonacularClient, ComplexSearchRequest


async def search_recipes(
    query: str,
    cuisine: Optional[str] = None,
    diet: Optional[str] = None,
    max_ready_time: Optional[int] = None,
    include_ingredients: Optional[str] = None,
    exclude_ingredients: Optional[str] = None,
    number: int = 10
) -> str:
    """
    Search for recipes using natural language parameters.
    
    Args:
        query: What to search for (e.g., "pasta", "chicken curry")
        cuisine: Type of cuisine (e.g., "italian", "indian", "mexican")
        diet: Dietary restriction (e.g., "vegetarian", "vegan", "gluten free")
        max_ready_time: Maximum cooking time in minutes
        include_ingredients: Comma-separated ingredients that must be included
        exclude_ingredients: Comma-separated ingredients to avoid
        number: Number of recipes to return (1-20)
        
    Returns:
        Formatted string with recipe search results
        
    Example:
        results = await search_recipes(
            query="pasta",
            cuisine="italian",
            max_ready_time=30,
            number=5
        )
    """
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        return "❌ Error: SPOONACULAR_API_KEY environment variable not set"
    
    try:
        # Convert string parameters to lists
        include_list = [i.strip() for i in include_ingredients.split(",")] if include_ingredients else None
        exclude_list = [i.strip() for i in exclude_ingredients.split(",")] if exclude_ingredients else None
        
        async with SpoonacularClient(api_key=api_key) as client:
            recipes_api = await client.recipes
            
            results = await recipes_api.complex_search(
                query=query,
                cuisine=cuisine,
                diet=diet,
                max_ready_time=max_ready_time,
                include_ingredients=include_list,
                exclude_ingredients=exclude_list,
                number=min(number, 20),  # Limit to 20 results
                add_recipe_information=True
            )
            
            if not results.results:
                return f"🔍 No recipes found for: {query}"
            
            # Format results
            output = [f"🍽️ Found {results.total_results} recipes for '{query}':\n"]
            
            for i, recipe in enumerate(results.results, 1):
                output.append(f"{i}. **{recipe.title}** (ID: {recipe.id})")
                
                details = []
                if recipe.ready_in_minutes:
                    details.append(f"⏱️ {recipe.ready_in_minutes} min")
                if recipe.servings:
                    details.append(f"👥 {recipe.servings} servings")
                if recipe.health_score:
                    details.append(f"🏥 Health: {recipe.health_score}/100")
                if recipe.price_per_serving:
                    details.append(f"💰 ${recipe.price_per_serving:.2f}/serving")
                
                if details:
                    output.append(f"   {' | '.join(details)}")
                
                # Add dietary info
                diet_tags = []
                if recipe.vegetarian:
                    diet_tags.append("🥬 Vegetarian")
                if recipe.vegan:
                    diet_tags.append("🌱 Vegan")
                if recipe.gluten_free:
                    diet_tags.append("🌾 Gluten-Free")
                if recipe.dairy_free:
                    diet_tags.append("🥛 Dairy-Free")
                if recipe.very_healthy:
                    diet_tags.append("💪 Very Healthy")
                
                if diet_tags:
                    output.append(f"   {' | '.join(diet_tags)}")
                
                # Add cuisines and dish types
                if recipe.cuisines:
                    output.append(f"   🌍 Cuisine: {', '.join(recipe.cuisines)}")
                if recipe.dish_types:
                    output.append(f"   🍽️ Type: {', '.join(recipe.dish_types)}")
                
                output.append("")  # Empty line between recipes
            
            return "\n".join(output)
            
    except Exception as e:
        return f"❌ Error searching recipes: {str(e)}"


async def get_recipe_details(recipe_id: int, include_nutrition: bool = True) -> str:
    """
    Get detailed information about a specific recipe.
    
    Args:
        recipe_id: The recipe ID from search results
        include_nutrition: Whether to include nutrition information
        
    Returns:
        Formatted string with detailed recipe information
        
    Example:
        details = await get_recipe_details(1096211, include_nutrition=True)
    """
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        return "❌ Error: SPOONACULAR_API_KEY environment variable not set"
    
    try:
        async with SpoonacularClient(api_key=api_key) as client:
            recipes_api = await client.recipes
            
            recipe = await recipes_api.get_recipe_information(
                recipe_id=recipe_id,
                include_nutrition=include_nutrition,
                add_wine_pairing=True,
                add_taste_data=False
            )
            
            output = [f"📋 **{recipe.title}**\n"]
            
            # Basic info
            if recipe.servings:
                output.append(f"👥 **Servings:** {recipe.servings}")
            if recipe.ready_in_minutes:
                output.append(f"⏱️ **Ready in:** {recipe.ready_in_minutes} minutes")
            if recipe.preparation_minutes:
                output.append(f"🔪 **Prep time:** {recipe.preparation_minutes} minutes")
            if recipe.cooking_minutes:
                output.append(f"🔥 **Cook time:** {recipe.cooking_minutes} minutes")
            
            # Scores and metrics
            if recipe.health_score:
                output.append(f"🏥 **Health Score:** {recipe.health_score}/100")
            if recipe.spoonacular_score:
                output.append(f"⭐ **Spoonacular Score:** {recipe.spoonacular_score}/100")
            if recipe.price_per_serving:
                output.append(f"💰 **Price per serving:** ${recipe.price_per_serving:.2f}")
            
            output.append("")  # Empty line
            
            # Dietary information
            diet_info = []
            if recipe.vegetarian:
                diet_info.append("🥬 Vegetarian")
            if recipe.vegan:
                diet_info.append("🌱 Vegan")
            if recipe.gluten_free:
                diet_info.append("🌾 Gluten-Free")
            if recipe.dairy_free:
                diet_info.append("🥛 Dairy-Free")
            if recipe.ketogenic:
                diet_info.append("🥓 Ketogenic")
            if recipe.whole30:
                diet_info.append("🍎 Whole30")
            if recipe.very_healthy:
                diet_info.append("💪 Very Healthy")
            
            if diet_info:
                output.append(f"🏷️ **Diet Tags:** {' | '.join(diet_info)}")
                output.append("")
            
            # Cuisines and dish types
            if recipe.cuisines:
                output.append(f"🌍 **Cuisines:** {', '.join(recipe.cuisines)}")
            if recipe.dish_types:
                output.append(f"🍽️ **Dish Types:** {', '.join(recipe.dish_types)}")
            if recipe.occasions:
                output.append(f"🎉 **Occasions:** {', '.join(recipe.occasions)}")
            
            output.append("")
            
            # Ingredients
            if recipe.extended_ingredients:
                output.append("🛒 **Ingredients:**")
                for ingredient in recipe.extended_ingredients:
                    if ingredient.original:
                        output.append(f"  • {ingredient.original}")
                output.append("")
            
            # Instructions
            if recipe.analyzed_instructions:
                output.append("👨‍🍳 **Instructions:**")
                for instruction_set in recipe.analyzed_instructions:
                    for step in instruction_set.steps:
                        output.append(f"  {step.number}. {step.step}")
                output.append("")
            elif recipe.instructions:
                output.append("👨‍🍳 **Instructions:**")
                # Clean up HTML if present
                instructions = recipe.instructions.replace('<ol>', '').replace('</ol>', '')
                instructions = instructions.replace('<li>', '• ').replace('</li>', '\n')
                output.append(instructions)
                output.append("")
            
            # Nutrition
            if recipe.nutrition and include_nutrition:
                output.append("📊 **Nutrition (per serving):**")
                
                # Key nutrients
                key_nutrients = ['Calories', 'Fat', 'Carbohydrates', 'Protein', 'Fiber', 'Sugar', 'Sodium']
                for nutrient_name in key_nutrients:
                    nutrient = next(
                        (n for n in recipe.nutrition.nutrients if n.name == nutrient_name),
                        None
                    )
                    if nutrient:
                        output.append(f"  • **{nutrient.name}:** {nutrient.amount:.1f}{nutrient.unit}")
                
                # Caloric breakdown
                if recipe.nutrition.caloric_breakdown:
                    cb = recipe.nutrition.caloric_breakdown
                    output.append(f"  • **Caloric Breakdown:** Protein {cb.percent_protein:.0f}% | Fat {cb.percent_fat:.0f}% | Carbs {cb.percent_carbs:.0f}%")
                
                output.append("")
            
            # Wine pairing
            if recipe.wine_pairing and recipe.wine_pairing.pairing_text:
                output.append("🍷 **Wine Pairing:**")
                output.append(f"  {recipe.wine_pairing.pairing_text}")
                if recipe.wine_pairing.paired_wines:
                    output.append(f"  **Recommended wines:** {', '.join(recipe.wine_pairing.paired_wines)}")
                output.append("")
            
            # Summary
            if recipe.summary:
                # Clean HTML tags from summary
                import re
                clean_summary = re.sub('<.*?>', '', recipe.summary)
                output.append("📝 **Summary:**")
                output.append(clean_summary)
                output.append("")
            
            # Source
            if recipe.source_name and recipe.source_url:
                output.append(f"🔗 **Source:** [{recipe.source_name}]({recipe.source_url})")
            elif recipe.spoonacular_source_url:
                output.append(f"🔗 **Source:** [Spoonacular]({recipe.spoonacular_source_url})")
            
            return "\n".join(output)
            
    except Exception as e:
        return f"❌ Error getting recipe details: {str(e)}"


def search_recipes_sync(
    query: str,
    cuisine: Optional[str] = None,
    diet: Optional[str] = None,
    max_ready_time: Optional[int] = None,
    include_ingredients: Optional[str] = None,
    exclude_ingredients: Optional[str] = None,
    number: int = 10
) -> str:
    """
    Synchronous version of search_recipes for use in non-async contexts.
    
    Args:
        query: What to search for (e.g., "pasta", "chicken curry")
        cuisine: Type of cuisine (e.g., "italian", "indian", "mexican")
        diet: Dietary restriction (e.g., "vegetarian", "vegan", "gluten free")
        max_ready_time: Maximum cooking time in minutes
        include_ingredients: Comma-separated ingredients that must be included
        exclude_ingredients: Comma-separated ingredients to avoid
        number: Number of recipes to return (1-20)
        
    Returns:
        Formatted string with recipe search results
    """
    try:
        # Try to run in new event loop
        return asyncio.run(search_recipes(
            query=query,
            cuisine=cuisine,
            diet=diet,
            max_ready_time=max_ready_time,
            include_ingredients=include_ingredients,
            exclude_ingredients=exclude_ingredients,
            number=number
        ))
    except RuntimeError:
        # If we're already in an event loop, create a task
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    search_recipes(
                        query=query,
                        cuisine=cuisine,
                        diet=diet,
                        max_ready_time=max_ready_time,
                        include_ingredients=include_ingredients,
                        exclude_ingredients=exclude_ingredients,
                        number=number
                    )
                )
                return future.result()
        else:
            raise


def get_recipe_details_sync(recipe_id: int, include_nutrition: bool = True) -> str:
    """
    Synchronous version of get_recipe_details for use in non-async contexts.
    
    Args:
        recipe_id: The recipe ID from search results
        include_nutrition: Whether to include nutrition information
        
    Returns:
        Formatted string with detailed recipe information
    """
    try:
        # Try to run in new event loop
        return asyncio.run(get_recipe_details(recipe_id, include_nutrition))
    except RuntimeError:
        # If we're already in an event loop, create a task
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    get_recipe_details(recipe_id, include_nutrition)
                )
                return future.result()
        else:
            raise


# Example usage
if __name__ == "__main__":
    async def demo():
        """Demonstrate the agent tools"""
        print("🔍 Searching for Italian pasta recipes...")
        search_result = await search_recipes(
            query="pasta",
            cuisine="italian",
            max_ready_time=30,
            number=3
        )
        print(search_result)
        
        print("\n" + "="*50)
        print("📋 Getting detailed recipe information...")
        
        # Extract first recipe ID from search result (simple parsing)
        import re
        id_match = re.search(r'ID: (\d+)', search_result)
        if id_match:
            recipe_id = int(id_match.group(1))
            details = await get_recipe_details(recipe_id, include_nutrition=True)
            print(details)
        else:
            print("No recipe ID found in search results")
    
    # Run demo if API key is available
    if os.getenv("SPOONACULAR_API_KEY"):
        asyncio.run(demo())
    else:
        print("Set SPOONACULAR_API_KEY environment variable to run the demo")