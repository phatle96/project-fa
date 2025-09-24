"""
Fresh Alert API Products endpoints.
"""

import logging
from typing import List, Optional, Dict, Any

from ..base_client import BaseHttpClient
from ..models import ProductResponseDto, ProductListResponse, ProductFilterParams
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