"""
Modular Spoonacular API Client

A well-structured, async-first Python client for the Spoonacular API.
Features clean separation of concerns, comprehensive error handling,
and both async and sync interfaces.

Example usage:
    # Async usage
    async with SpoonacularClient(api_key="your-key") as client:
        recipes_api = await client.recipes
        results = await recipes_api.complex_search(query="pasta")
        
    # Sync usage  
    client = SpoonacularClient(api_key="your-key")
    results = client.sync.recipes.complex_search(query="pasta")
    
    # Using convenience function
    client = create_client(api_key="your-key")
"""

from .client import SpoonacularClient, SyncSpoonacularClient, create_client
from .config import SpoonacularConfig
from .exceptions import (
    SpoonacularError,
    SpoonacularAPIError,
    SpoonacularAuthenticationError,
    SpoonacularRateLimitError,
    SpoonacularConnectionError
)
from .models import (
    # Request models
    ComplexSearchRequest,
    RecipeInformationRequest,
    FindByIngredientsRequest,
    
    # Response models
    ComplexSearchResponse,
    Recipe,
    SimilarRecipe,
    SimilarRecipesResponse,
    RandomRecipesResponse,
    AutocompleteRecipe,
    AutocompleteResponse,
    FindByIngredientsResponse,
    RecipeByIngredients,
    IngredientUsage,
    
    # Common models
    ExtendedIngredient,
    Equipment,
    RecipeInstruction,
    NutritionInfo,
    
    # Enums
    Cuisine,
    Diet,
    Intolerance,
    MealType,
    RecipeSortOption as RecipeSort
)

__version__ = "1.0.0"

__all__ = [
    # Main client classes
    "SpoonacularClient",
    "SyncSpoonacularClient", 
    "create_client",
    
    # Configuration
    "SpoonacularConfig",
    
    # Exceptions
    "SpoonacularError",
    "SpoonacularAPIError",
    "SpoonacularAuthenticationError",
    "SpoonacularRateLimitError",
    "SpoonacularConnectionError",
    
    # Request models
    "ComplexSearchRequest",
    "RecipeInformationRequest",
    "FindByIngredientsRequest",
    
    # Response models
    "ComplexSearchResponse",
    "Recipe",
    "SimilarRecipe",
    "SimilarRecipesResponse", 
    "RandomRecipesResponse",
    "AutocompleteRecipe",
    "AutocompleteResponse",
    "FindByIngredientsResponse",
    "RecipeByIngredients",
    "IngredientUsage",
    
    # Common models
    "ExtendedIngredient",
    "Equipment",
    "RecipeInstruction",
    "NutritionInfo",
    
    # Enums
    "Cuisine",
    "Diet",
    "Intolerance",
    "MealType",
    "RecipeSort"
]