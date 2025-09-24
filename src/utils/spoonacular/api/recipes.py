"""
Recipes API client for Spoonacular API.

This module provides methods for recipe-related endpoints including
complex search and detailed recipe information.
"""

import logging
from typing import Optional, Dict, Any, List, Union

from ..base_client import BaseHttpClient
from ..config import SpoonacularConfig, ClientDefaults
from ..models import (
    ComplexSearchRequest,
    ComplexSearchResponse,
    RecipeInformationRequest,
    Recipe,
    SimilarRecipe,
    SimilarRecipesResponse,
    RandomRecipesResponse,
    AutocompleteRecipe,
    AutocompleteResponse,
    FindByIngredientsRequest,
    FindByIngredientsResponse
)

logger = logging.getLogger(__name__)


class RecipesAPI:
    """Client for recipe-related API endpoints"""
    
    def __init__(self, http_client: BaseHttpClient):
        self.http_client = http_client
    
    async def complex_search(
        self,
        request: Optional[ComplexSearchRequest] = None,
        **kwargs
    ) -> ComplexSearchResponse:
        """
        Search recipes using advanced filtering and ranking.
        
        This method combines searching by query, by ingredients, and by nutrients.
        
        Args:
            request: ComplexSearchRequest object with search parameters
            **kwargs: Individual search parameters (alternative to request object)
            
        Returns:
            ComplexSearchResponse with search results
            
        Example:
            # Using request object
            search_request = ComplexSearchRequest(
                query="pasta",
                cuisine=["italian"],
                diet=["vegetarian"],
                max_ready_time=30,
                number=20
            )
            results = await recipes_api.complex_search(search_request)
            
            # Using kwargs
            results = await recipes_api.complex_search(
                query="chicken curry",
                cuisine="indian",
                max_ready_time=45,
                add_recipe_information=True
            )
        """
        # Combine request object and kwargs
        if request:
            params = request.model_dump(exclude_none=True)
        else:
            params = {}
        
        # Override with any kwargs
        params.update({k: v for k, v in kwargs.items() if v is not None})
        
        # Convert parameter names to match API expectations
        api_params = self._convert_search_params(params)
        
        logger.debug(f"Making complex search with params: {api_params}")
        
        response_data = await self.http_client.get(
            endpoint=ClientDefaults.ENDPOINTS["recipes_complex_search"],
            params=api_params
        )
        
        return ComplexSearchResponse(**response_data)
    
    async def get_recipe_information(
        self,
        recipe_id: int,
        include_nutrition: bool = False,
        add_wine_pairing: bool = False,
        add_taste_data: bool = False
    ) -> Recipe:
        """
        Get detailed information about a specific recipe.
        
        Args:
            recipe_id: The recipe ID
            include_nutrition: Whether to include nutrition data
            add_wine_pairing: Whether to include wine pairing information
            add_taste_data: Whether to include taste information
            
        Returns:
            Recipe object with detailed information
            
        Example:
            recipe = await recipes_api.get_recipe_information(
                recipe_id=1096211,
                include_nutrition=True,
                add_wine_pairing=True
            )
        """
        params = {
            "includeNutrition": include_nutrition,
            "addWinePairing": add_wine_pairing,
            "addTasteData": add_taste_data
        }
        
        logger.debug(f"Getting recipe information for ID: {recipe_id}")
        
        response_data = await self.http_client.get(
            endpoint=ClientDefaults.ENDPOINTS["recipe_information"],
            path_params={"id": recipe_id},
            params=params
        )
        
        return Recipe(**response_data)
    
    async def find_by_ingredients(
        self,
        ingredients: Union[str, List[str]],
        number: int = 10,
        ranking: int = 1,
        ignore_pantry: bool = True
    ) -> FindByIngredientsResponse:
        """
        Find recipes based on available ingredients.
        
        This method searches for recipes that use the provided ingredients,
        showing which ingredients are used and which are missing.
        
        Args:
            ingredients: Ingredients to search with (string or list)
            number: Number of recipes to return (1-100)
            ranking: Ranking optimization (1=maximize used ingredients, 2=minimize missing)
            ignore_pantry: Whether to ignore common pantry items
            
        Returns:
            FindByIngredientsResponse with recipes and ingredient usage
            
        Example:
            # Using string
            results = await recipes_api.find_by_ingredients(
                ingredients="carrots,tomatoes,onions",
                number=20,
                ranking=1
            )
            
            # Using list
            results = await recipes_api.find_by_ingredients(
                ingredients=["carrots", "tomatoes", "onions"],
                ranking=2
            )
        """
        # Convert list to comma-separated string if needed
        if isinstance(ingredients, list):
            ingredients_str = ",".join(ingredients)
        else:
            ingredients_str = ingredients
            
        params = {
            "ingredients": ingredients_str,
            "number": number,
            "ranking": ranking,
            "ignorePantry": ignore_pantry
        }
        
        logger.debug(f"Finding recipes with ingredients: {ingredients_str}")
        
        response_data = await self.http_client.get(
            endpoint=ClientDefaults.ENDPOINTS["recipes_find_by_ingredients"],
            params=params
        )
        
        # The API returns a list directly, so we wrap it in our response model
        return FindByIngredientsResponse(recipes_data=response_data)
    
    async def get_similar_recipes(
        self,
        recipe_id: int,
        number: int = 10
    ) -> SimilarRecipesResponse:
        """
        Get recipes similar to a given recipe.
        
        Args:
            recipe_id: The recipe ID to find similar recipes for
            number: Number of similar recipes to return
            
        Returns:
            SimilarRecipesResponse with similar recipes
        """
        params = {"number": number}
        
        response_data = await self.http_client.get(
            endpoint=ClientDefaults.ENDPOINTS["recipe_similar"],
            path_params={"id": recipe_id},
            params=params
        )
        
        return SimilarRecipesResponse(recipes=response_data)
    
    async def get_random_recipes(
        self,
        number: int = 10,
        include_tags: Optional[Union[str, List[str]]] = None,
        exclude_tags: Optional[Union[str, List[str]]] = None
    ) -> RandomRecipesResponse:
        """
        Get random recipes.
        
        Args:
            number: Number of random recipes to return
            include_tags: Tags that recipes must have
            exclude_tags: Tags that recipes must not have
            
        Returns:
            RandomRecipesResponse with random recipes
        """
        params = {"number": number}
        
        if include_tags:
            if isinstance(include_tags, list):
                params["include-tags"] = ",".join(include_tags)
            else:
                params["include-tags"] = include_tags
        
        if exclude_tags:
            if isinstance(exclude_tags, list):
                params["exclude-tags"] = ",".join(exclude_tags)
            else:
                params["exclude-tags"] = exclude_tags
        
        response_data = await self.http_client.get(
            endpoint=ClientDefaults.ENDPOINTS["recipes_random"],
            params=params
        )
        
        return RandomRecipesResponse(recipes=response_data.get("recipes", []))
    
    async def autocomplete_recipe_search(
        self,
        query: str,
        number: int = 10
    ) -> AutocompleteResponse:
        """
        Autocomplete recipe search for partial queries.
        
        Args:
            query: Partial recipe name or query
            number: Number of suggestions to return
            
        Returns:
            AutocompleteResponse with recipe suggestions
        """
        params = {
            "query": query,
            "number": number
        }
        
        response_data = await self.http_client.get(
            endpoint=ClientDefaults.ENDPOINTS["recipes_autocomplete"],
            params=params
        )
        
        return AutocompleteResponse(suggestions=response_data)
    
    def _convert_search_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Convert parameter names from snake_case to API format"""
        api_params = {}
        
        # Parameter name mapping
        param_mapping = {
            "exclude_cuisine": "excludeCuisine",
            "include_ingredients": "includeIngredients", 
            "exclude_ingredients": "excludeIngredients",
            "instructions_required": "instructionsRequired",
            "fill_ingredients": "fillIngredients",
            "add_recipe_information": "addRecipeInformation",
            "add_recipe_nutrition": "addRecipeNutrition",
            "recipe_box_id": "recipeBoxId",
            "title_match": "titleMatch",
            "max_ready_time": "maxReadyTime",
            "min_ready_time": "minReadyTime",
            "ignore_pantry": "ignorePantry",
            "sort_direction": "sortDirection",
            "limit_license": "limitLicense"
        }
        
        for key, value in params.items():
            # Use mapping if available, otherwise convert snake_case to camelCase
            if key in param_mapping:
                api_key = param_mapping[key]
            elif "_" in key:
                # Convert snake_case to camelCase for nutrient parameters
                parts = key.split("_")
                api_key = parts[0] + "".join(word.capitalize() for word in parts[1:])
            else:
                api_key = key
            
            api_params[api_key] = value
        
        return api_params