"""
Main Spoonacular API client.

This module provides a unified interface to all Spoonacular API endpoints
with both async and sync support.
"""

import asyncio
import logging
from typing import Optional, Any, Dict
from contextlib import asynccontextmanager

from .config import SpoonacularConfig
from .base_client import BaseHttpClient
from .api import RecipesAPI
from .models import *
from .exceptions import SpoonacularError

logger = logging.getLogger(__name__)


class SpoonacularClient:
    """
    Main Spoonacular API client with unified interface.
    
    This client provides access to all Spoonacular API endpoints through
    dedicated API classes. It supports both async and sync usage patterns.
    
    Example:
        # Async usage
        async with SpoonacularClient(api_key="your-api-key") as client:
            results = await client.recipes.complex_search(query="pasta")
            recipe = await client.recipes.get_recipe_information(results.results[0].id)
        
        # Sync usage
        client = SpoonacularClient(api_key="your-api-key")
        results = client.sync.recipes.complex_search(query="pasta")
        recipe = client.sync.recipes.get_recipe_information(results.results[0].id)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[SpoonacularConfig] = None,
        **config_kwargs
    ):
        """
        Initialize the Spoonacular client.
        
        Args:
            api_key: Spoonacular API key (overrides config)
            config: SpoonacularConfig object
            **config_kwargs: Additional config parameters
        """
        if config is None:
            config = SpoonacularConfig(**config_kwargs)
        
        if api_key:
            config.api_key = api_key
        
        if not config.api_key:
            raise ValueError("API key is required. Set SPOONACULAR_API_KEY environment variable or pass api_key parameter.")
        
        self.config = config
        self._http_client: Optional[BaseHttpClient] = None
        self._recipes: Optional[RecipesAPI] = None
        self._sync_client: Optional['SyncSpoonacularClient'] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_http_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._http_client:
            await self._http_client.close()
    
    async def _ensure_http_client(self):
        """Ensure HTTP client is initialized"""
        if self._http_client is None:
            self._http_client = BaseHttpClient(self.config)
    
    @property
    async def recipes(self) -> RecipesAPI:
        """Get recipes API instance"""
        await self._ensure_http_client()
        if self._recipes is None:
            self._recipes = RecipesAPI(self._http_client)
        return self._recipes
    
    @property
    def sync(self) -> 'SyncSpoonacularClient':
        """Get synchronous client wrapper"""
        if self._sync_client is None:
            self._sync_client = SyncSpoonacularClient(self)
        return self._sync_client
    
    async def close(self):
        """Close the HTTP client"""
        if self._http_client:
            await self._http_client.close()


class SyncSpoonacularClient:
    """
    Synchronous wrapper for SpoonacularClient.
    
    This class provides synchronous methods by wrapping the async client
    and running methods in an event loop.
    """
    
    def __init__(self, async_client: SpoonacularClient):
        self._async_client = async_client
        self._recipes: Optional['SyncRecipesAPI'] = None
    
    @property
    def recipes(self) -> 'SyncRecipesAPI':
        """Get synchronous recipes API"""
        if self._recipes is None:
            self._recipes = SyncRecipesAPI(self._async_client)
        return self._recipes


class SyncRecipesAPI:
    """Synchronous wrapper for RecipesAPI"""
    
    def __init__(self, async_client: SpoonacularClient):
        self._async_client = async_client
    
    def complex_search(self, **kwargs) -> ComplexSearchResponse:
        """Synchronous complex search"""
        return asyncio.run(self._complex_search(**kwargs))
    
    async def _complex_search(self, **kwargs) -> ComplexSearchResponse:
        """Internal async method for complex search"""
        async with self._async_client as client:
            recipes_api = await client.recipes
            return await recipes_api.complex_search(**kwargs)
    
    def get_recipe_information(
        self,
        recipe_id: int,
        include_nutrition: bool = False,
        add_wine_pairing: bool = False,
        add_taste_data: bool = False
    ) -> Recipe:
        """Synchronous get recipe information"""
        return asyncio.run(self._get_recipe_information(
            recipe_id, include_nutrition, add_wine_pairing, add_taste_data
        ))
    
    async def _get_recipe_information(
        self,
        recipe_id: int,
        include_nutrition: bool = False,
        add_wine_pairing: bool = False,
        add_taste_data: bool = False
    ) -> Recipe:
        """Internal async method for get recipe information"""
        async with self._async_client as client:
            recipes_api = await client.recipes
            return await recipes_api.get_recipe_information(
                recipe_id, include_nutrition, add_wine_pairing, add_taste_data
            )
    
    def get_similar_recipes(self, recipe_id: int, number: int = 10) -> SimilarRecipesResponse:
        """Synchronous get similar recipes"""
        return asyncio.run(self._get_similar_recipes(recipe_id, number))
    
    async def _get_similar_recipes(self, recipe_id: int, number: int = 10) -> SimilarRecipesResponse:
        """Internal async method for get similar recipes"""
        async with self._async_client as client:
            recipes_api = await client.recipes
            return await recipes_api.get_similar_recipes(recipe_id, number)
    
    def get_random_recipes(self, **kwargs) -> RandomRecipesResponse:
        """Synchronous get random recipes"""
        return asyncio.run(self._get_random_recipes(**kwargs))
    
    async def _get_random_recipes(self, **kwargs) -> RandomRecipesResponse:
        """Internal async method for get random recipes"""
        async with self._async_client as client:
            recipes_api = await client.recipes
            return await recipes_api.get_random_recipes(**kwargs)
    
    def autocomplete_recipe_search(self, query: str, number: int = 10) -> AutocompleteResponse:
        """Synchronous autocomplete recipe search"""
        return asyncio.run(self._autocomplete_recipe_search(query, number))
    
    async def _autocomplete_recipe_search(self, query: str, number: int = 10) -> AutocompleteResponse:
        """Internal async method for autocomplete recipe search"""
        async with self._async_client as client:
            recipes_api = await client.recipes
            return await recipes_api.autocomplete_recipe_search(query, number)


# Convenience function for quick access
def create_client(api_key: Optional[str] = None, **config_kwargs) -> SpoonacularClient:
    """
    Create a Spoonacular client with simplified configuration.
    
    Args:
        api_key: Spoonacular API key
        **config_kwargs: Additional configuration options
        
    Returns:
        SpoonacularClient instance
        
    Example:
        client = create_client(api_key="your-api-key", timeout=30)
    """
    return SpoonacularClient(api_key=api_key, **config_kwargs)