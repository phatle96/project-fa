"""
Common data models used across different API endpoints.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict


class NutritionInfo(BaseModel):
    """Nutrition information for a single nutrient"""
    
    name: str = Field(description="Name of the nutrient")
    amount: float = Field(description="Amount of the nutrient")
    unit: str = Field(description="Unit of measurement")
    percent_of_daily_needs: Optional[float] = Field(
        default=None, 
        alias="percentOfDailyNeeds",
        description="Percentage of daily recommended intake"
    )
    
    model_config = ConfigDict(populate_by_name=True)


class CaloricBreakdown(BaseModel):
    """Caloric breakdown by macronutrients"""
    
    percent_protein: Optional[float] = Field(default=None, alias="percentProtein")
    percent_fat: Optional[float] = Field(default=None, alias="percentFat") 
    percent_carbs: Optional[float] = Field(default=None, alias="percentCarbs")
    
    model_config = ConfigDict(populate_by_name=True)


class WeightPerServing(BaseModel):
    """Weight information per serving"""
    
    amount: Optional[float] = Field(default=None)
    unit: Optional[str] = Field(default=None)


class Measures(BaseModel):
    """Measurement information for ingredients"""
    
    us: Optional[Dict[str, Any]] = Field(default=None, description="US measurements")
    metric: Optional[Dict[str, Any]] = Field(default=None, description="Metric measurements")


class IngredientMeasure(BaseModel):
    """Individual measurement for an ingredient"""
    
    amount: Optional[float] = Field(default=None)
    unit_short: Optional[str] = Field(default=None, alias="unitShort")
    unit_long: Optional[str] = Field(default=None, alias="unitLong")
    
    model_config = ConfigDict(populate_by_name=True)


class Equipment(BaseModel):
    """Equipment used in recipe preparation"""
    
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    local_name: Optional[str] = Field(default=None, alias="localizedName")
    image: Optional[str] = Field(default=None)
    temperature: Optional[Dict[str, Any]] = Field(default=None)
    
    model_config = ConfigDict(populate_by_name=True)


class IngredientInfo(BaseModel):
    """Basic ingredient information used in instructions"""
    
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    local_name: Optional[str] = Field(default=None, alias="localizedName")
    image: Optional[str] = Field(default=None)
    
    model_config = ConfigDict(populate_by_name=True)


class Length(BaseModel):
    """Time length information"""
    
    number: Optional[int] = Field(default=None)
    unit: Optional[str] = Field(default=None)


class RecipeStep(BaseModel):
    """Individual step in recipe instructions"""
    
    number: int = Field(description="Step number")
    step: str = Field(description="Step instructions")
    ingredients: Optional[List[IngredientInfo]] = Field(
        default_factory=list,
        description="Ingredients used in this step"
    )
    equipment: Optional[List[Equipment]] = Field(
        default_factory=list,
        description="Equipment used in this step"
    )
    length: Optional[Length] = Field(default=None, description="Time required for this step")


class RecipeInstruction(BaseModel):
    """Recipe instructions with steps"""
    
    name: Optional[str] = Field(default=None, description="Name of instruction set")
    steps: List[RecipeStep] = Field(
        default_factory=list,
        description="List of instruction steps"
    )


class TasteInfo(BaseModel):
    """Taste profile information"""
    
    sweetness: Optional[float] = Field(default=None)
    saltiness: Optional[float] = Field(default=None)
    sourness: Optional[float] = Field(default=None)
    bitterness: Optional[float] = Field(default=None)
    savoriness: Optional[float] = Field(default=None)
    fattiness: Optional[float] = Field(default=None)
    spiciness: Optional[float] = Field(default=None)


class WinePairing(BaseModel):
    """Wine pairing information"""
    
    paired_wines: Optional[List[str]] = Field(default_factory=list, alias="pairedWines")
    pairing_text: Optional[str] = Field(default=None, alias="pairingText")
    product_matches: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, 
        alias="productMatches"
    )
    
    model_config = ConfigDict(populate_by_name=True)