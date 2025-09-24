"""
Model exports for Spoonacular API client.

This module provides a clean interface to import all model classes
without needing to know the internal file structure.
"""

# Enums
from .enums import (
    SortDirection,
    RecipeSortOption,
    Diet,
    Intolerance,
    MealType,
    Cuisine,
    EquipmentType,
    DishType
)

# Common models
from .common import (
    NutritionInfo,
    CaloricBreakdown,
    WeightPerServing,
    Measures,
    IngredientMeasure,
    Equipment,
    IngredientInfo,
    Length,
    RecipeStep,
    RecipeInstruction,
    TasteInfo,
    WinePairing
)

# Request models
from .requests import (
    ComplexSearchRequest,
    RecipeInformationRequest,
    FindByIngredientsRequest
)

# Response models
from .responses import (
    RecipeNutrition,
    ExtendedIngredient,
    Recipe,
    ComplexSearchResponse,
    RecipeInformationResponse,
    SimilarRecipe,
    SimilarRecipesResponse,
    RandomRecipesResponse,
    AutocompleteRecipe,
    AutocompleteResponse,
    IngredientUsage,
    RecipeByIngredients,
    FindByIngredientsResponse
)

__all__ = [
    # Enums
    "SortDirection",
    "RecipeSortOption", 
    "Diet",
    "Intolerance",
    "MealType",
    "Cuisine",
    "EquipmentType",
    "DishType",
    
    # Common models
    "NutritionInfo",
    "CaloricBreakdown",
    "WeightPerServing",
    "Measures",
    "IngredientMeasure",
    "Equipment",
    "IngredientInfo",
    "Length",
    "RecipeStep",
    "RecipeInstruction",
    "TasteInfo",
    "WinePairing",
    
    # Request models
    "ComplexSearchRequest",
    "RecipeInformationRequest",
    "FindByIngredientsRequest",
    
    # Response models
    "RecipeNutrition",
    "ExtendedIngredient",
    "Recipe",
    "ComplexSearchResponse",
    "RecipeInformationResponse",
    "SimilarRecipe",
    "SimilarRecipesResponse",
    "RandomRecipesResponse",
    "AutocompleteRecipe",
    "AutocompleteResponse",
    "IngredientUsage",
    "RecipeByIngredients",
    "FindByIngredientsResponse"
]