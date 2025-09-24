"""
Request models for Spoonacular API endpoints.
"""

from typing import List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict

from .enums import (
    Diet, Cuisine, MealType, Intolerance, RecipeSortOption, 
    SortDirection, EquipmentType, DishType
)


class ComplexSearchRequest(BaseModel):
    """Request model for complex recipe search"""
    
    # Basic search parameters
    query: Optional[str] = Field(None, description="Natural language search query")
    number: Optional[int] = Field(10, description="Number of results to return (1-100)")
    offset: Optional[int] = Field(None, description="Number of results to skip (0-900)")
    
    # Dietary and cuisine filters
    cuisine: Optional[Union[Cuisine, List[Cuisine], str]] = Field(
        None, description="Cuisine type(s) to include"
    )
    exclude_cuisine: Optional[Union[Cuisine, List[Cuisine], str]] = Field(
        None, description="Cuisine type(s) to exclude"
    )
    diet: Optional[Union[Diet, List[Diet], str]] = Field(
        None, description="Diet type(s) for the recipes"
    )
    intolerances: Optional[Union[Intolerance, List[Intolerance], str]] = Field(
        None, description="Food intolerances to avoid"
    )
    
    # Recipe type and equipment
    type: Optional[Union[MealType, List[MealType], str]] = Field(
        None, description="Type of recipe/meal"
    )
    equipment: Optional[Union[str, List[str]]] = Field(
        None, description="Required equipment"
    )
    
    # Ingredients
    include_ingredients: Optional[Union[str, List[str]]] = Field(
        None, description="Ingredients that must be included"
    )
    exclude_ingredients: Optional[Union[str, List[str]]] = Field(
        None, description="Ingredients to exclude"
    )
    
    # Time constraints
    max_ready_time: Optional[int] = Field(
        None, description="Maximum preparation and cooking time in minutes"
    )
    min_ready_time: Optional[int] = Field(
        None, description="Minimum preparation and cooking time in minutes"
    )
    
    # Additional options
    instructions_required: Optional[bool] = Field(
        None, description="Only return recipes with instructions"
    )
    fill_ingredients: Optional[bool] = Field(
        None, description="Add ingredient usage information"
    )
    add_recipe_information: Optional[bool] = Field(
        None, description="Include detailed recipe information"
    )
    add_recipe_nutrition: Optional[bool] = Field(
        None, description="Include nutrition information"
    )
    
    # Authoring and filtering
    author: Optional[str] = Field(None, description="Recipe author username")
    tags: Optional[Union[str, List[str]]] = Field(
        None, description="Recipe tags (diets, meal types, cuisines, intolerances)"
    )
    recipe_box_id: Optional[int] = Field(None, description="Recipe box ID to limit search")
    title_match: Optional[str] = Field(
        None, description="Text that must appear in recipe title"
    )
    
    # Sorting
    sort: Optional[RecipeSortOption] = Field(None, description="Sort strategy")
    sort_direction: Optional[SortDirection] = Field(None, description="Sort direction")
    
    # Nutrition filters - Macronutrients
    min_carbs: Optional[float] = Field(None, description="Minimum carbohydrates (g)")
    max_carbs: Optional[float] = Field(None, description="Maximum carbohydrates (g)")
    min_protein: Optional[float] = Field(None, description="Minimum protein (g)")
    max_protein: Optional[float] = Field(None, description="Maximum protein (g)")
    min_calories: Optional[float] = Field(None, description="Minimum calories")
    max_calories: Optional[float] = Field(None, description="Maximum calories")
    min_fat: Optional[float] = Field(None, description="Minimum fat (g)")
    max_fat: Optional[float] = Field(None, description="Maximum fat (g)")
    min_saturated_fat: Optional[float] = Field(None, description="Minimum saturated fat (g)")
    max_saturated_fat: Optional[float] = Field(None, description="Maximum saturated fat (g)")
    min_fiber: Optional[float] = Field(None, description="Minimum fiber (g)")
    max_fiber: Optional[float] = Field(None, description="Maximum fiber (g)")
    min_sugar: Optional[float] = Field(None, description="Minimum sugar (g)")
    max_sugar: Optional[float] = Field(None, description="Maximum sugar (g)")
    
    # Nutrition filters - Vitamins
    min_vitamin_a: Optional[float] = Field(None, description="Minimum Vitamin A (IU)")
    max_vitamin_a: Optional[float] = Field(None, description="Maximum Vitamin A (IU)")
    min_vitamin_c: Optional[float] = Field(None, description="Minimum Vitamin C (mg)")
    max_vitamin_c: Optional[float] = Field(None, description="Maximum Vitamin C (mg)")
    min_vitamin_d: Optional[float] = Field(None, description="Minimum Vitamin D (µg)")
    max_vitamin_d: Optional[float] = Field(None, description="Maximum Vitamin D (µg)")
    min_vitamin_e: Optional[float] = Field(None, description="Minimum Vitamin E (mg)")
    max_vitamin_e: Optional[float] = Field(None, description="Maximum Vitamin E (mg)")
    min_vitamin_k: Optional[float] = Field(None, description="Minimum Vitamin K (µg)")
    max_vitamin_k: Optional[float] = Field(None, description="Maximum Vitamin K (µg)")
    min_vitamin_b1: Optional[float] = Field(None, description="Minimum Vitamin B1 (mg)")
    max_vitamin_b1: Optional[float] = Field(None, description="Maximum Vitamin B1 (mg)")
    min_vitamin_b2: Optional[float] = Field(None, description="Minimum Vitamin B2 (mg)")
    max_vitamin_b2: Optional[float] = Field(None, description="Maximum Vitamin B2 (mg)")
    min_vitamin_b3: Optional[float] = Field(None, description="Minimum Vitamin B3 (mg)")
    max_vitamin_b3: Optional[float] = Field(None, description="Maximum Vitamin B3 (mg)")
    min_vitamin_b5: Optional[float] = Field(None, description="Minimum Vitamin B5 (mg)")
    max_vitamin_b5: Optional[float] = Field(None, description="Maximum Vitamin B5 (mg)")
    min_vitamin_b6: Optional[float] = Field(None, description="Minimum Vitamin B6 (mg)")
    max_vitamin_b6: Optional[float] = Field(None, description="Maximum Vitamin B6 (mg)")
    min_vitamin_b12: Optional[float] = Field(None, description="Minimum Vitamin B12 (µg)")
    max_vitamin_b12: Optional[float] = Field(None, description="Maximum Vitamin B12 (µg)")
    min_folate: Optional[float] = Field(None, description="Minimum folate (µg)")
    max_folate: Optional[float] = Field(None, description="Maximum folate (µg)")
    min_folic_acid: Optional[float] = Field(None, description="Minimum folic acid (µg)")
    max_folic_acid: Optional[float] = Field(None, description="Maximum folic acid (µg)")
    
    # Nutrition filters - Minerals
    min_calcium: Optional[float] = Field(None, description="Minimum calcium (mg)")
    max_calcium: Optional[float] = Field(None, description="Maximum calcium (mg)")
    min_copper: Optional[float] = Field(None, description="Minimum copper (mg)")
    max_copper: Optional[float] = Field(None, description="Maximum copper (mg)")
    min_iron: Optional[float] = Field(None, description="Minimum iron (mg)")
    max_iron: Optional[float] = Field(None, description="Maximum iron (mg)")
    min_magnesium: Optional[float] = Field(None, description="Minimum magnesium (mg)")
    max_magnesium: Optional[float] = Field(None, description="Maximum magnesium (mg)")
    min_manganese: Optional[float] = Field(None, description="Minimum manganese (mg)")
    max_manganese: Optional[float] = Field(None, description="Maximum manganese (mg)")
    min_phosphorus: Optional[float] = Field(None, description="Minimum phosphorus (mg)")
    max_phosphorus: Optional[float] = Field(None, description="Maximum phosphorus (mg)")
    min_potassium: Optional[float] = Field(None, description="Minimum potassium (mg)")
    max_potassium: Optional[float] = Field(None, description="Maximum potassium (mg)")
    min_selenium: Optional[float] = Field(None, description="Minimum selenium (µg)")
    max_selenium: Optional[float] = Field(None, description="Maximum selenium (µg)")
    min_sodium: Optional[float] = Field(None, description="Minimum sodium (mg)")
    max_sodium: Optional[float] = Field(None, description="Maximum sodium (mg)")
    min_zinc: Optional[float] = Field(None, description="Minimum zinc (mg)")
    max_zinc: Optional[float] = Field(None, description="Maximum zinc (mg)")
    
    # Other nutrients
    min_alcohol: Optional[float] = Field(None, description="Minimum alcohol (g)")
    max_alcohol: Optional[float] = Field(None, description="Maximum alcohol (g)")
    min_caffeine: Optional[float] = Field(None, description="Minimum caffeine (mg)")
    max_caffeine: Optional[float] = Field(None, description="Maximum caffeine (mg)")
    min_choline: Optional[float] = Field(None, description="Minimum choline (mg)")
    max_choline: Optional[float] = Field(None, description="Maximum choline (mg)")
    min_cholesterol: Optional[float] = Field(None, description="Minimum cholesterol (mg)")
    max_cholesterol: Optional[float] = Field(None, description="Maximum cholesterol (mg)")
    min_fluoride: Optional[float] = Field(None, description="Minimum fluoride (mg)")
    max_fluoride: Optional[float] = Field(None, description="Maximum fluoride (mg)")
    min_iodine: Optional[float] = Field(None, description="Minimum iodine (µg)")
    max_iodine: Optional[float] = Field(None, description="Maximum iodine (µg)")
    
    # Additional options
    ignore_pantry: Optional[bool] = Field(
        None, description="Ignore typical pantry items"
    )
    limit_license: Optional[bool] = Field(
        None, description="Only return recipes with open license"
    )
    
    model_config = ConfigDict(use_enum_values=True)


class RecipeInformationRequest(BaseModel):
    """Request model for getting detailed recipe information"""
    
    recipe_id: int = Field(description="Recipe ID")
    include_nutrition: Optional[bool] = Field(
        False, description="Include nutrition data"
    )
    add_wine_pairing: Optional[bool] = Field(
        False, description="Include wine pairing information"
    )
    add_taste_data: Optional[bool] = Field(
        False, description="Include taste information"
    )
    
    model_config = ConfigDict(use_enum_values=True)


class FindByIngredientsRequest(BaseModel):
    """Request model for finding recipes by ingredients"""
    
    ingredients: str = Field(
        description="Comma-separated list of ingredients (e.g., 'carrots,tomatoes,onions')"
    )
    number: Optional[int] = Field(
        10, description="Number of recipes to return (1-100)"
    )
    ranking: Optional[int] = Field(
        1, description="Ranking optimization (1=maximize used ingredients, 2=minimize missing ingredients)"
    )
    ignore_pantry: Optional[bool] = Field(
        True, description="Whether to ignore common pantry items like salt, water, etc."
    )
    
    model_config = ConfigDict(use_enum_values=True)