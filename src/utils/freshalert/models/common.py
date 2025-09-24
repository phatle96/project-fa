"""
Common Pydantic models used across Fresh Alert API.
"""

from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    """Standard API response wrapper"""
    res: int = Field(..., description="Response status (1 for success, 0 for error)")
    error: Optional[str] = Field(None, description="Error message if any")
    error_code: Optional[str] = Field(None, alias="errorCode", description="Error code if any")
    access_token: Optional[str] = Field(None, alias="accessToken", description="Access token if provided")
    data: Optional[Any] = Field(None, description="Response data")
    
    class Config:
        allow_population_by_field_name = True


class DateResponseModel(BaseModel):
    """Date tracking information for products"""
    id: str = Field(..., description="Unique identifier")
    product_id: str = Field(..., alias="productId", description="Product ID (UUID)")
    date_manufactured: Optional[datetime] = Field(None, alias="dateManufactured", description="Manufacturing date")
    date_best_before: Optional[datetime] = Field(None, alias="dateBestBefore", description="Best before date")
    date_expired: Optional[datetime] = Field(None, alias="dateExpired", description="Expiration date")
    quantity: Optional[float] = Field(None, description="Product quantity")
    
    class Config:
        allow_population_by_field_name = True


class ProductResponseDto(BaseModel):
    """Product information response"""
    id: str = Field(..., description="Product unique identifier")
    code_number: Optional[str] = Field(None, alias="codeNumber", description="Product barcode/code")
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
    date_product_users: Optional[List[DateResponseModel]] = Field(
        None, 
        alias="dateProductUsers", 
        description="Date tracking entries for this product"
    )
    
    class Config:
        allow_population_by_field_name = True


class ProductListResponse(BaseModel):
    """Response for product list endpoints"""
    res: int = Field(..., description="Response status")
    error: Optional[str] = Field(None, description="Error message if any")
    error_code: Optional[str] = Field(None, alias="errorCode", description="Error code if any")
    data: List[ProductResponseDto] = Field(default_factory=list, description="List of products")
    
    class Config:
        allow_population_by_field_name = True