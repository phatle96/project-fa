"""
Response models for Fresh Alert API endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field
from .common import ProductResponseDto, ProductListResponse, ResponseModel, DateResponseModel


class ProductCodeResponse(BaseModel):
    """Response for product code search endpoint"""
    res: int = Field(..., description="Response status (1 for success, 0 for error)")
    error: Optional[str] = Field(None, description="Error message if any")
    error_code: Optional[str] = Field(None, alias="errorCode", description="Error code if any")
    data: Optional[ProductResponseDto] = Field(None, description="Product data")
    
    model_config = {
        "populate_by_name": True
    }


class CreateProductCodeResponse(BaseModel):
    """Response for product code creation endpoint"""
    res: int = Field(..., description="Response status (1 for success, 0 for error)")
    error: Optional[str] = Field(None, description="Error message if any")
    error_code: Optional[str] = Field(None, alias="errorCode", description="Error code if any")
    data: Optional[ProductResponseDto] = Field(None, description="Created product data")
    
    model_config = {
        "populate_by_name": True
    }


class CreateProductDateResponse(BaseModel):
    """Response for product date creation endpoint"""
    res: int = Field(..., description="Response status (1 for success, 0 for error)")
    error: Optional[str] = Field(None, description="Error message if any")
    error_code: Optional[str] = Field(None, alias="errorCode", description="Error code if any")
    data: Optional[DateResponseModel] = Field(None, description="Created date entry data")
    
    model_config = {
        "populate_by_name": True
    }


class UpdateProductDateResponse(BaseModel):
    """Response for product date update endpoint"""
    res: int = Field(..., description="Response status (1 for success, 0 for error)")
    error: Optional[str] = Field(None, description="Error message if any")
    error_code: Optional[str] = Field(None, alias="errorCode", description="Error code if any")
    data: Optional[DateResponseModel] = Field(None, description="Updated date entry data")
    
    model_config = {
        "populate_by_name": True
    }


class DeleteProductResponse(BaseModel):
    """Response for product deletion endpoint"""
    res: int = Field(..., description="Response status (1 for success, 0 for error)")
    error: Optional[str] = Field(None, description="Error message if any")
    error_code: Optional[str] = Field(None, alias="errorCode", description="Error code if any")
    data: Optional[dict] = Field(None, description="Deletion confirmation data")
    
    model_config = {
        "populate_by_name": True
    }


__all__ = [
    "ProductResponseDto",
    "ProductListResponse", 
    "ResponseModel",
    "DateResponseModel",
    "ProductCodeResponse",
    "CreateProductCodeResponse",
    "CreateProductDateResponse",
    "UpdateProductDateResponse",
    "DeleteProductResponse"
]