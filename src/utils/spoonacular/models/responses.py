"""
Response models for Spoonacular API endpoints.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from .common import (
    NutritionInfo, CaloricBreakdown, WeightPerServing, 
    RecipeInstruction, TasteInfo, WinePairing, Measures
)


class RecipeNutrition(BaseModel):
    """Complete nutrition information for a recipe"""
    
    nutrients: List[NutritionInfo] = Field(default_factory=list)
    properties: Optional[List[NutritionInfo]] = Field(default_factory=list)
    flavonoids: Optional[List[NutritionInfo]] = Field(default_factory=list)
    ingredients: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    caloric_breakdown: Optional[CaloricBreakdown] = Field(
        default=None, alias="caloricBreakdown"
    )
    weight_per_serving: Optional[WeightPerServing] = Field(
        default=None, alias="weightPerServing"
    )
    
    model_config = ConfigDict(populate_by_name=True)


class ExtendedIngredient(BaseModel):
    """Extended ingredient information with measurements"""
    
    id: Optional[int] = Field(default=None)
    aisle: Optional[str] = Field(default="")  # Allow empty string instead of None
    image: Optional[str] = Field(default="")  # Allow empty string instead of None
    consistency: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    name_clean: Optional[str] = Field(default=None, alias="nameClean")
    original: Optional[str] = Field(default=None)
    original_name: Optional[str] = Field(default=None, alias="originalName")
    amount: Optional[float] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    meta: Optional[List[str]] = Field(default_factory=list)
    measures: Optional[Measures] = Field(default=None)
    
    model_config = ConfigDict(populate_by_name=True)


class Recipe(BaseModel):
    """Recipe information from search results or detailed view"""
    
    # Basic information
    id: int = Field(description="Recipe ID")
    title: str = Field(description="Recipe title")
    image: Optional[str] = Field(default=None, description="Recipe image URL")
    image_type: Optional[str] = Field(default=None, alias="imageType")
    
    # Timing and serving information
    servings: Optional[int] = Field(default=None)
    ready_in_minutes: Optional[int] = Field(default=None, alias="readyInMinutes")
    preparation_minutes: Optional[int] = Field(default=None, alias="preparationMinutes")
    cooking_minutes: Optional[int] = Field(default=None, alias="cookingMinutes")
    
    # Source and licensing
    license: Optional[str] = Field(default=None)
    source_name: Optional[str] = Field(default=None, alias="sourceName")
    source_url: Optional[str] = Field(default=None, alias="sourceUrl")
    spoonacular_source_url: Optional[str] = Field(
        default=None, alias="spoonacularSourceUrl"
    )
    
    # Popularity and scoring
    aggregate_likes: Optional[int] = Field(default=None, alias="aggregateLikes")
    health_score: Optional[float] = Field(default=None, alias="healthScore")
    spoonacular_score: Optional[float] = Field(default=None, alias="spoonacularScore")
    price_per_serving: Optional[float] = Field(default=None, alias="pricePerServing")
    
    # Content
    instructions: Optional[str] = Field(default=None)
    analyzed_instructions: Optional[List[RecipeInstruction]] = Field(
        default_factory=list, alias="analyzedInstructions"
    )
    
    # Recipe properties
    cheap: Optional[bool] = Field(default=None)
    credits_text: Optional[str] = Field(default=None, alias="creditsText")
    cuisines: Optional[List[str]] = Field(default_factory=list)
    dish_types: Optional[List[str]] = Field(default_factory=list, alias="dishTypes")
    diets: Optional[List[str]] = Field(default_factory=list)
    occasions: Optional[List[str]] = Field(default_factory=list)
    
    # Dietary information
    dairy_free: Optional[bool] = Field(default=None, alias="dairyFree")
    gluten_free: Optional[bool] = Field(default=None, alias="glutenFree")
    ketogenic: Optional[bool] = Field(default=None)
    low_fodmap: Optional[bool] = Field(default=None, alias="lowFodmap")
    vegan: Optional[bool] = Field(default=None)
    vegetarian: Optional[bool] = Field(default=None)
    very_healthy: Optional[bool] = Field(default=None, alias="veryHealthy")
    very_popular: Optional[bool] = Field(default=None, alias="veryPopular")
    whole30: Optional[bool] = Field(default=None)
    sustainable: Optional[bool] = Field(default=None)
    
    # Additional information
    gaps: Optional[str] = Field(default=None)
    weight_watcher_smart_points: Optional[int] = Field(
        default=None, alias="weightWatcherSmartPoints"
    )
    
    # Complex data
    extended_ingredients: Optional[List[ExtendedIngredient]] = Field(
        default_factory=list, alias="extendedIngredients"
    )
    summary: Optional[str] = Field(default=None)
    wine_pairing: Optional[WinePairing] = Field(default=None, alias="winePairing")
    taste: Optional[TasteInfo] = Field(default=None)
    nutrition: Optional[RecipeNutrition] = Field(default=None)
    
    model_config = ConfigDict(populate_by_name=True)


class ComplexSearchResponse(BaseModel):
    """Response model for complex recipe search"""
    
    results: List[Recipe] = Field(default_factory=list)
    offset: int = Field(default=0)
    number: int = Field(default=10) 
    total_results: int = Field(alias="totalResults")
    
    model_config = ConfigDict(populate_by_name=True)


class RecipeInformationResponse(BaseModel):
    """Response model for detailed recipe information"""
    
    recipe: Recipe = Field(description="Detailed recipe information")
    
    model_config = ConfigDict(populate_by_name=True)


class SimilarRecipe(BaseModel):
    """Similar recipe information"""
    
    id: int
    title: str
    image_type: Optional[str] = Field(default=None, alias="imageType")
    ready_in_minutes: Optional[int] = Field(default=None, alias="readyInMinutes")
    servings: Optional[int] = Field(default=None)
    source_url: Optional[str] = Field(default=None, alias="sourceUrl")
    
    model_config = ConfigDict(populate_by_name=True)


class SimilarRecipesResponse(BaseModel):
    """Response model for similar recipes"""
    
    recipes: List[SimilarRecipe] = Field(default_factory=list)


class RandomRecipesResponse(BaseModel):
    """Response model for random recipes"""
    
    recipes: List[Recipe] = Field(default_factory=list)


class AutocompleteRecipe(BaseModel):
    """Autocomplete recipe suggestion"""
    
    id: int
    title: str
    image_type: Optional[str] = Field(default=None, alias="imageType")
    
    model_config = ConfigDict(populate_by_name=True)


class AutocompleteResponse(BaseModel):
    """Response model for recipe autocomplete"""
    
    suggestions: List[AutocompleteRecipe] = Field(default_factory=list)


class IngredientUsage(BaseModel):
    """Information about ingredient usage in a recipe"""
    
    id: int
    amount: float
    unit: str
    unit_long: Optional[str] = Field(default=None, alias="unitLong")
    unit_short: Optional[str] = Field(default=None, alias="unitShort")
    aisle: Optional[str] = Field(default=None)
    name: str
    original: str
    original_name: Optional[str] = Field(default=None, alias="originalName")
    meta: Optional[List[str]] = Field(default_factory=list)
    image: Optional[str] = Field(default=None)
    
    model_config = ConfigDict(populate_by_name=True)


class RecipeByIngredients(BaseModel):
    """Recipe found by ingredients with usage information"""
    
    id: int
    title: str
    image: Optional[str] = Field(default=None)
    image_type: Optional[str] = Field(default=None, alias="imageType")
    used_ingredient_count: int = Field(alias="usedIngredientCount")
    missed_ingredient_count: int = Field(alias="missedIngredientCount")
    used_ingredients: List[IngredientUsage] = Field(
        default_factory=list, alias="usedIngredients"
    )
    missed_ingredients: List[IngredientUsage] = Field(
        default_factory=list, alias="missedIngredients"
    )
    likes: Optional[int] = Field(default=0)
    
    model_config = ConfigDict(populate_by_name=True)


class FindByIngredientsResponse(BaseModel):
    """Response model for find recipes by ingredients"""
    
    recipes: List[RecipeByIngredients] = Field(default_factory=list)
    
    def __init__(self, recipes_data: List[Dict[str, Any]] = None, **data):
        """Custom initialization to handle direct list response from API"""
        if recipes_data is not None:
            super().__init__(recipes=recipes_data, **data)
        else:
            super().__init__(**data)