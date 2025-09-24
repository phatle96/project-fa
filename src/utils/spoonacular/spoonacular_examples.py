"""
Comprehensive examples for the Spoonacular API client.

This file demonstrates various usage patterns for the modular Spoonacular client,
including both async and sync patterns, error handling, and different search options.
"""

import asyncio
import os
from typing import List
from pprint import pprint

# Add the project root to Python path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.spoonacular import (
    SpoonacularClient,
    create_client,
    ComplexSearchRequest,
    Cuisine,
    Diet,
    RecipeSort,
    SpoonacularException
)


async def async_examples():
    """Demonstrate async usage patterns"""
    
    print("=== Async Examples ===\n")
    
    # Create client with environment variable or pass API key directly
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        print("Please set SPOONACULAR_API_KEY environment variable")
        return
    
    # Example 1: Basic complex search with context manager
    print("1. Basic Complex Search:")
    async with SpoonacularClient(api_key=api_key) as client:
        recipes_api = await client.recipes
        
        results = await recipes_api.complex_search(
            query="pasta",
            number=5,
            add_recipe_information=True
        )
        
        print(f"Found {results.total_results} recipes")
        for recipe in results.results[:3]:
            print(f"- {recipe.title} (ID: {recipe.id})")
    
    print()
    
    # Example 2: Advanced search with request object
    print("2. Advanced Search with Request Object:")
    async with SpoonacularClient(api_key=api_key) as client:
        recipes_api = await client.recipes
        
        search_request = ComplexSearchRequest(
            query="chicken curry",
            cuisine=[Cuisine.INDIAN, Cuisine.THAI],
            diet=[Diet.GLUTEN_FREE],
            max_ready_time=45,
            min_carbs=20,
            max_carbs=50,
            sort=RecipeSort.POPULARITY,
            sort_direction="desc",
            number=10,
            add_recipe_information=True
        )
        
        results = await search_request.execute(recipes_api)
        
        print(f"Found {len(results.results)} gluten-free chicken curry recipes")
        for recipe in results.results[:3]:
            print(f"- {recipe.title} ({recipe.ready_in_minutes} min)")
    
    print()
    
    # Example 3: Get detailed recipe information
    print("3. Detailed Recipe Information:")
    async with SpoonacularClient(api_key=api_key) as client:
        recipes_api = await client.recipes
        
        # First search for a recipe
        search_results = await recipes_api.complex_search(
            query="chocolate cake",
            number=1
        )
        
        if search_results.results:
            recipe_id = search_results.results[0].id
            
            # Get detailed information
            detailed_recipe = await recipes_api.get_recipe_information(
                recipe_id=recipe_id,
                include_nutrition=True,
                add_wine_pairing=True
            )
            
            print(f"Recipe: {detailed_recipe.title}")
            print(f"Ready in: {detailed_recipe.ready_in_minutes} minutes")
            print(f"Servings: {detailed_recipe.servings}")
            
            if detailed_recipe.wine_pairing:
                print(f"Wine pairing: {detailed_recipe.wine_pairing.pairing_text}")
    
    print()
    
    # Example 4: Similar and random recipes
    print("4. Similar and Random Recipes:")
    async with SpoonacularClient(api_key=api_key) as client:
        recipes_api = await client.recipes
        
        # Get random recipes
        random_recipes = await recipes_api.get_random_recipes(
            number=3,
            include_tags=["vegetarian", "healthy"]
        )
        
        print(f"Random vegetarian recipes:")
        for recipe in random_recipes.recipes[:2]:
            print(f"- {recipe.title}")
            
            # Get similar recipes
            similar = await recipes_api.get_similar_recipes(
                recipe_id=recipe.id,
                number=2
            )
            
            print("  Similar recipes:")
            for sim_recipe in similar.recipes:
                print(f"    - {sim_recipe.title}")
    
    print()


def sync_examples():
    """Demonstrate synchronous usage patterns"""
    
    print("=== Sync Examples ===\n")
    
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        print("Please set SPOONACULAR_API_KEY environment variable")
        return
    
    # Example 1: Sync complex search
    print("1. Sync Complex Search:")
    client = create_client(api_key=api_key)
    
    results = client.sync.recipes.complex_search(
        query="italian pasta",
        cuisine="italian",
        number=5
    )
    
    print(f"Found {results.total_results} Italian pasta recipes")
    for recipe in results.results[:3]:
        print(f"- {recipe.title}")
    
    print()
    
    # Example 2: Sync recipe information
    print("2. Sync Recipe Information:")
    if results.results:
        recipe_id = results.results[0].id
        
        detailed_recipe = client.sync.recipes.get_recipe_information(
            recipe_id=recipe_id,
            include_nutrition=True
        )
        
        print(f"Recipe: {detailed_recipe.title}")
        print(f"Ingredients: {len(detailed_recipe.extended_ingredients)}")
        
        if detailed_recipe.nutrition:
            calories = next(
                (nutrient.amount for nutrient in detailed_recipe.nutrition.nutrients 
                 if nutrient.name == "Calories"), 
                None
            )
            if calories:
                print(f"Calories: {calories}")
    
    print()


async def error_handling_examples():
    """Demonstrate error handling patterns"""
    
    print("=== Error Handling Examples ===\n")
    
    # Example with invalid API key
    print("1. Invalid API Key:")
    try:
        async with SpoonacularClient(api_key="invalid-key") as client:
            recipes_api = await client.recipes
            await recipes_api.complex_search(query="test")
    except SpoonacularException as e:
        print(f"Caught expected error: {e}")
    
    print()
    
    # Example with invalid recipe ID
    print("2. Invalid Recipe ID:")
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if api_key:
        try:
            async with SpoonacularClient(api_key=api_key) as client:
                recipes_api = await client.recipes
                await recipes_api.get_recipe_information(recipe_id=999999999)
        except SpoonacularException as e:
            print(f"Caught expected error: {e}")
    
    print()


async def advanced_search_examples():
    """Demonstrate advanced search capabilities"""
    
    print("=== Advanced Search Examples ===\n")
    
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        print("Please set SPOONACULAR_API_KEY environment variable")
        return
    
    async with SpoonacularClient(api_key=api_key) as client:
        recipes_api = await client.recipes
        
        # Example 1: Nutrient-based search
        print("1. Nutrient-based Search (High Protein, Low Carb):")
        results = await recipes_api.complex_search(
            min_protein=30,  # At least 30g protein
            max_carbs=20,    # Max 20g carbs
            number=5,
            add_recipe_information=True
        )
        
        for recipe in results.results:
            print(f"- {recipe.title}")
        
        print()
        
        # Example 2: Ingredient inclusion/exclusion
        print("2. Include/Exclude Ingredients:")
        results = await recipes_api.complex_search(
            include_ingredients=["chicken", "garlic"],
            exclude_ingredients=["nuts", "dairy"],
            number=5
        )
        
        for recipe in results.results:
            print(f"- {recipe.title}")
        
        print()
        
        # Example 3: Multiple dietary restrictions
        print("3. Multiple Dietary Restrictions:")
        search_request = ComplexSearchRequest(
            diet=[Diet.VEGETARIAN, Diet.GLUTEN_FREE],
            intolerances=["dairy", "egg"],
            max_ready_time=30,
            number=5
        )
        
        results = await search_request.execute(recipes_api)
        
        for recipe in results.results:
            print(f"- {recipe.title} ({recipe.ready_in_minutes} min)")
        
        print()
        
        # Example 4: Autocomplete search
        print("4. Autocomplete Search:")
        suggestions = await recipes_api.autocomplete_recipe_search(
            query="choc",
            number=5
        )
        
        print("Suggestions for 'choc':")
        for suggestion in suggestions.suggestions:
            print(f"- {suggestion.title}")


async def main():
    """Run all examples"""
    print("Spoonacular API Client Examples")
    print("=" * 40)
    print()
    
    await async_examples()
    sync_examples()
    await error_handling_examples()
    await advanced_search_examples()
    
    print("\nAll examples completed!")


if __name__ == "__main__":
    # Set up logging to see what's happening
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Run examples
    asyncio.run(main())