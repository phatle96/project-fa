"""
Main Fresh Alert API client.
"""

import logging
from typing import Optional, List

from .config import FreshAlertConfig
from .base_client import BaseHttpClient
from .api import ProductsAPI
from .models import ProductResponseDto
from .exceptions import FreshAlertError

logger = logging.getLogger(__name__)


class FreshAlertClient:
    """
    Main client for Fresh Alert API.
    
    This class provides a unified interface to all Fresh Alert API endpoints
    with automatic authentication, error handling, and rate limiting.
    
    Example:
        >>> from freshalert import FreshAlertClient, FreshAlertConfig
        >>> 
        >>> config = FreshAlertConfig(bearer_token="your-token-here")
        >>> client = FreshAlertClient(config)
        >>> 
        >>> async with client:
        >>>     # Get all user products
        >>>     products = await client.products.get_user_products()
        >>>     
        >>>     # Get products expiring in the next 7 days
        >>>     expiring = await client.products.get_expired_products(days=7)
    """
    
    def __init__(self, config: Optional[FreshAlertConfig] = None):
        """
        Initialize the Fresh Alert client.
        
        Args:
            config (Optional[FreshAlertConfig]): Configuration object.
                If None, will create default config (loads from environment variables).
        """
        self.config = config or FreshAlertConfig()
        self._http_client: Optional[BaseHttpClient] = None
        self._products_api: Optional[ProductsAPI] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_initialized()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def _ensure_initialized(self):
        """Ensure the HTTP client is initialized"""
        if self._http_client is None:
            self._http_client = BaseHttpClient(self.config)
            self._products_api = ProductsAPI(self._http_client)
    
    async def close(self):
        """Close the HTTP client and clean up resources"""
        if self._http_client:
            await self._http_client.close()
            self._http_client = None
            self._products_api = None
    
    @property
    def products(self) -> ProductsAPI:
        """
        Access to product-related API endpoints.
        
        Returns:
            ProductsAPI: API client for product endpoints
            
        Raises:
            RuntimeError: If client is not initialized (use async context manager)
        """
        if self._products_api is None:
            raise RuntimeError(
                "Client not initialized. Use 'async with FreshAlertClient() as client:' "
                "or call 'await client._ensure_initialized()' first."
            )
        return self._products_api
    
    # Convenience methods for common operations
    
    async def get_my_products(self) -> List[ProductResponseDto]:
        """
        Convenience method to get all products for the current user.
        
        Returns:
            List[ProductResponseDto]: List of user's products
            
        Raises:
            FreshAlertError: If the request fails
        """
        await self._ensure_initialized()
        return await self.products.get_user_products()
    
    async def get_expiring_products(self, days: int = 7) -> List[ProductResponseDto]:
        """
        Convenience method to get products expiring within specified days.
        
        Args:
            days (int): Number of days to look ahead (default: 7)
            
        Returns:
            List[ProductResponseDto]: List of expiring products
            
        Raises:
            FreshAlertError: If the request fails
        """
        await self._ensure_initialized()
        return await self.products.get_expired_products(days=days)
    
    async def get_expired_products(self) -> List[ProductResponseDto]:
        """
        Convenience method to get products that are already expired.
        
        Returns:
            List[ProductResponseDto]: List of expired products
            
        Raises:
            FreshAlertError: If the request fails
        """
        await self._ensure_initialized()
        return await self.products.get_expired_products()
    
    # Utility methods
    
    def is_authenticated(self) -> bool:
        """
        Check if the client has authentication credentials.
        
        Returns:
            bool: True if bearer token or API key is configured
        """
        return bool(self.config.bearer_token or self.config.api_key)
    
    async def health_check(self) -> bool:
        """
        Perform a health check by making a simple API request.
        
        Returns:
            bool: True if the API is accessible and authentication works
            
        Raises:
            FreshAlertError: If the health check fails
        """
        try:
            await self._ensure_initialized()
            # Try to get user products as a health check
            await self.products.get_user_products()
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise
    
    def __repr__(self) -> str:
        """String representation of the client"""
        auth_status = "authenticated" if self.is_authenticated() else "not authenticated"
        return f"FreshAlertClient(base_url='{self.config.base_url}', {auth_status})"