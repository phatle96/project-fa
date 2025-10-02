"""
Fresh Alert API Products endpoints.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..base_client import BaseHttpClient
from ..models import (
    ProductResponseDto, 
    ProductListResponse,
    PaginatedProductResponse,
    ProductFilterParams,
    CreateProductCodeRequest,
    CreateProductDateRequest,
    UpdateProductDateRequest,
    ProductCodeResponse,
    CreateProductCodeResponse,
    CreateProductDateResponse,
    UpdateProductDateResponse,
    DeleteProductResponse,
    DateResponseModel,
    ProductSearchServiceResponse
)
from ..exceptions import FreshAlertAPIError

logger = logging.getLogger(__name__)


class ProductsAPI:
    """API client for Fresh Alert product endpoints"""
    
    def __init__(self, client: BaseHttpClient):
        self.client = client
    
    async def get_user_products(self) -> List[ProductResponseDto]:
        """
        Get all products for the current user.
        
        Endpoint: GET /product/user
        
        Returns:
            List[ProductResponseDto]: List of user's products
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        try:
            logger.info("Fetching user products")
            
            response_data = await self.client.get("/product/user")
            
            # Parse the response using our models
            response = ProductListResponse(**response_data)
            
            if response.res != 1:
                error_msg = response.error or "Failed to fetch user products"
                raise FreshAlertAPIError(
                    message=error_msg,
                    error_code=response.error_code,
                    response_data=response_data
                )
            
            logger.info(f"Retrieved {len(response.data)} user products")
            return response.data
            
        except Exception as e:
            if isinstance(e, FreshAlertAPIError):
                raise
            
            logger.error(f"Error fetching user products: {e}")
            raise FreshAlertAPIError(f"Failed to fetch user products: {str(e)}")
    
    async def get_expired_products(self, days: Optional[int] = None) -> List[ProductResponseDto]:
        """
        Get products that are expired or about to expire for the current user.
        
        Endpoint: GET /product/user/expired
        
        Args:
            days (Optional[int]): Number of days for lookback (optional query parameter)
            
        Returns:
            List[ProductResponseDto]: List of expired/expiring products
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        try:
            logger.info(f"Fetching expired products (days={days})")
            
            # Prepare query parameters
            params = {}
            if days is not None:
                params["days"] = days
            
            response_data = await self.client.get("/product/user/expired", params=params)
            
            # Parse the response using our models
            response = ProductListResponse(**response_data)
            
            if response.res != 1:
                error_msg = response.error or "Failed to fetch expired products"
                raise FreshAlertAPIError(
                    message=error_msg,
                    error_code=response.error_code,
                    response_data=response_data
                )
            
            logger.info(f"Retrieved {len(response.data)} expired/expiring products")
            return response.data
            
        except Exception as e:
            if isinstance(e, FreshAlertAPIError):
                raise
            
            logger.error(f"Error fetching expired products: {e}")
            raise FreshAlertAPIError(f"Failed to fetch expired products: {str(e)}")
    
    async def get_expiring_products(self, days: int = 7) -> List[ProductResponseDto]:
        """
        Convenience method to get products expiring within a specific number of days.
        
        This is a wrapper around get_expired_products() with a default of 7 days.
        
        Args:
            days (int): Number of days to look ahead for expiring products (default: 7)
            
        Returns:
            List[ProductResponseDto]: List of products expiring within the specified days
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        return await self.get_expired_products(days=days)
    
    async def search_product_code(self, code: str) -> Optional[ProductResponseDto]:
        """
        Search for a product by its barcode/code number.
        
        Endpoint: GET /product-code/{code}
        
        Args:
            code (str): The product code/barcode to search for
            
        Returns:
            Optional[ProductResponseDto]: Product data if found, None otherwise
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        try:
            logger.info(f"Searching for product with code: {code}")
            
            response_data = await self.client.get(f"/product-code/{code}")
            
            # Parse the response using our models
            response = ProductCodeResponse(**response_data)
            
            if response.res != 1:
                error_msg = response.error or f"Product with code {code} not found"
                logger.warning(f"Product code search failed: {error_msg}")
                return None
            
            logger.info(f"Found product for code: {code}")
            return response.data
            
        except Exception as e:
            if isinstance(e, FreshAlertAPIError):
                raise
            
            logger.error(f"Error searching product code {code}: {e}")
            raise FreshAlertAPIError(f"Failed to search product code {code}: {str(e)}")
    
    async def create_product_code(self, product_data: CreateProductCodeRequest) -> ProductResponseDto:
        """
        Create a new product code entry.
        
        Endpoint: POST /product-code
        
        Args:
            product_data (CreateProductCodeRequest): Product data for creation
            
        Returns:
            ProductResponseDto: Created product data
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        try:
            logger.info(f"Creating product code: {product_data.code_number}")
            
            # Convert the request model to dict for API call
            request_data = product_data.model_dump(by_alias=True, exclude_none=True)
            
            response_data = await self.client.post("/product-code", json=request_data)
            
            # Parse the response using our models
            response = CreateProductCodeResponse(**response_data)
            
            if response.res != 1:
                error_msg = response.error or "Failed to create product code"
                raise FreshAlertAPIError(
                    message=error_msg,
                    error_code=response.error_code,
                    response_data=response_data
                )
            
            logger.info(f"Successfully created product code: {product_data.code_number}")
            return response.data
            
        except Exception as e:
            if isinstance(e, FreshAlertAPIError):
                raise
            
            logger.error(f"Error creating product code {product_data.code_number}: {e}")
            raise FreshAlertAPIError(f"Failed to create product code: {str(e)}")
    
    async def create_product_date(self, date_data: CreateProductDateRequest) -> Optional[DateResponseModel]:
        """
        Create a new product date entry.
        
        Endpoint: POST /date
        
        Args:
            date_data (CreateProductDateRequest): Date data for creation
            
        Returns:
            Optional[DateResponseModel]: Created date entry data
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        try:
            logger.info(f"Creating product date entry for product: {date_data.product_id}")
            
            # Convert the request model to dict for API call with proper datetime handling
            request_data = date_data.model_dump(by_alias=True, exclude_none=True)
            
            # Manually convert datetime objects to ISO format strings
            for key, value in request_data.items():
                if isinstance(value, datetime):
                    request_data[key] = value.isoformat()
            
            response_data = await self.client.post("/date", json=request_data)
            
            # Parse the response using our models
            response = CreateProductDateResponse(**response_data)
            
            if response.res != 1:
                error_msg = response.error or "Failed to create product date"
                raise FreshAlertAPIError(
                    message=error_msg,
                    error_code=response.error_code,
                    response_data=response_data
                )
            
            logger.info(f"Successfully created product date entry for: {date_data.product_id}")
            return response.data
            
        except Exception as e:
            if isinstance(e, FreshAlertAPIError):
                raise
            
            logger.error(f"Error creating product date for {date_data.product_id}: {e}")
            raise FreshAlertAPIError(f"Failed to create product date: {str(e)}")
    
    async def search_product_by_name(self, query: str) -> List[ProductSearchServiceResponse]:
        """
        Search for products by name or query string.
        
        Endpoint: GET /product-code/search/{query}
        
        Args:
            query (str): Search query string (product name or partial name)
            
        Returns:
            List[ProductResponseDto]: List of matching products
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        try:
            logger.info(f"Searching products with query: {query}")
            
            response_data = await self.client.get(f"/product-code/search/{query}")
            
            # Parse the response using paginated model (search returns paginated data)
            response = PaginatedProductResponse(**response_data)
            
            if response.res != 1:
                error_msg = response.error or f"Failed to search products with query: {query}"
                raise FreshAlertAPIError(
                    message=error_msg,
                    error_code=response.error_code,
                    response_data=response_data
                )
            
            # Extract the product list from paginated data
            products = response.data.products
            logger.info(f"Found {len(products)} products matching query: {query} (total: {response.data.count})")
            return products
            
        except Exception as e:
            if isinstance(e, FreshAlertAPIError):
                raise
            
            logger.error(f"Error searching products with query {query}: {e}")
            raise FreshAlertAPIError(f"Failed to search products: {str(e)}")
    
    async def update_product_date(self, date_id: str, date_data: UpdateProductDateRequest) -> Optional[DateResponseModel]:
        """
        Update an existing product date entry.
        
        Endpoint: PUT /date/{id}
        
        Args:
            date_id (str): ID of the date entry to update
            date_data (UpdateProductDateRequest): Updated date data
            
        Returns:
            Optional[DateResponseModel]: Updated date entry data
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        try:
            logger.info(f"Updating product date entry: {date_id}")
            
            # Convert the request model to dict for API call with proper datetime handling
            request_data = date_data.model_dump(by_alias=True, exclude_none=True)
            
            # Manually convert datetime objects to ISO format strings
            for key, value in request_data.items():
                if isinstance(value, datetime):
                    request_data[key] = value.isoformat()
            
            response_data = await self.client.put(f"/date/{date_id}", json=request_data)
            
            # Parse the response using our models
            response = UpdateProductDateResponse(**response_data)
            
            if response.res != 1:
                error_msg = response.error or "Failed to update product date"
                raise FreshAlertAPIError(
                    message=error_msg,
                    error_code=response.error_code,
                    response_data=response_data
                )
            
            logger.info(f"Successfully updated product date entry: {date_id}")
            return response.data
            
        except Exception as e:
            if isinstance(e, FreshAlertAPIError):
                raise
            
            logger.error(f"Error updating product date {date_id}: {e}")
            raise FreshAlertAPIError(f"Failed to update product date: {str(e)}")
    
    async def delete_product(self, product_id: str) -> Dict[str, Any]:
        """
        Soft delete a product from the user's list.
        
        Endpoint: DELETE /product/soft-delete/{id}
        
        Args:
            product_id (str): ID of the product to delete
            
        Returns:
            Dict[str, Any]: Deletion confirmation data
            
        Raises:
            FreshAlertAPIError: If the request fails
        """
        try:
            logger.info(f"Soft deleting product: {product_id}")
            
            response_data = await self.client.delete(f"/product/soft-delete/{product_id}")
            
            # Parse the response using our models
            response = DeleteProductResponse(**response_data)
            
            if response.res != 1:
                error_msg = response.error or "Failed to delete product"
                raise FreshAlertAPIError(
                    message=error_msg,
                    error_code=response.error_code,
                    response_data=response_data
                )
            
            logger.info(f"Successfully deleted product: {product_id}")
            return response.data or {"deleted": True, "product_id": product_id}
            
        except Exception as e:
            if isinstance(e, FreshAlertAPIError):
                raise
            
            logger.error(f"Error deleting product {product_id}: {e}")
            raise FreshAlertAPIError(f"Failed to delete product: {str(e)}")