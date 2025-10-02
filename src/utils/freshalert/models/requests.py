"""
Request models for Fresh Alert API endpoints.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .common import IngredientDto


class ProductFilterParams(BaseModel):
    """Query parameters for filtering products"""
    days: Optional[int] = Field(None, description="Number of days for lookback (used in expired endpoint)")
    
    model_config = {
        "extra": "forbid"  # Don't allow extra fields
    }





class CreateProductCodeRequest(BaseModel):
    """Request model for creating a product code"""
    code_number: str = Field(..., alias="codeNumber", description="Product barcode/code number")
    code_type: Optional[str] = Field(None, alias="codeType", description="Type of code (UPC, EAN, etc.)")
    product_name: Optional[str] = Field(None, alias="productName", description="Product name")
    brand: Optional[str] = Field(None, description="Product brand")
    manufacturer: Optional[str] = Field(None, description="Product manufacturer")
    description: Optional[str] = Field(None, description="Product description")
    image_url: Optional[List[str]] = Field(None, alias="imageUrl", description="Product images")
    usage_instruction: Optional[str] = Field(None, alias="usageInstruction", description="Usage instructions")
    storage_instruction: Optional[str] = Field(None, alias="storageInstruction", description="Storage instructions")
    country_of_origin: Optional[str] = Field(None, alias="countryOfOrigin", description="Country of origin")
    category: Optional[str] = Field(None, description="Product category")
    nutrition_fact: Optional[str] = Field(None, alias="nutritionFact", description="Nutrition facts")
    label_key: Optional[str] = Field(None, alias="labelKey", description="Label key")
    phrase: Optional[str] = Field(None, description="Key phrase")
    ingredients: Optional[List[IngredientDto]] = Field(None, description="Product ingredients")
    
    model_config = {
        "populate_by_name": True,
        "validate_by_name": True
    }


class CreateProductDateRequest(BaseModel):
    """Request model for creating a product date entry"""
    product_id: str = Field(..., alias="productId", description="Product ID (UUID)")
    date_manufactured: Optional[datetime] = Field(None, alias="dateManufactured", description="Manufacturing date")
    date_best_before: Optional[datetime] = Field(None, alias="dateBestBefore", description="Best before date")
    date_expired: Optional[datetime] = Field(None, alias="dateExpired", description="Expiration date")
    quantity: Optional[float] = Field(None, description="Product quantity")
    
    model_config = {
        "populate_by_name": True,
        "validate_by_name": True
    }


class UpdateProductDateRequest(BaseModel):
    """Request model for updating a product date entry"""
    product_id: str = Field(..., alias="productId", description="Product ID (UUID)")
    date_manufactured: Optional[datetime] = Field(None, alias="dateManufactured", description="Manufacturing date")
    date_best_before: Optional[datetime] = Field(None, alias="dateBestBefore", description="Best before date")
    date_expired: Optional[datetime] = Field(None, alias="dateExpired", description="Expiration date")
    quantity: Optional[float] = Field(None, description="Product quantity")
    
    model_config = {
        "populate_by_name": True,
        "validate_by_name": True
    }
