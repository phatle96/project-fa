"""
Base client configuration and settings for Spoonacular API.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class SpoonacularConfig(BaseSettings):
    """Configuration settings for Spoonacular API client"""
    
    api_key: Optional[str] = Field(default=None, description="Spoonacular API key")
    base_url: str = Field(default="https://api.spoonacular.com", description="Base API URL")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    rate_limit_delay: float = Field(default=0.1, description="Delay between requests")
    max_retries: int = Field(default=3, description="Maximum number of retries for failed requests")
    
    class Config:
        env_prefix = "SPOONACULAR_"
        env_file = ".env"
        case_sensitive = False

    @classmethod
    def from_env(cls) -> "SpoonacularConfig":
        """Create config from environment variables"""
        return cls()
    
    @classmethod
    def from_api_key(cls, api_key: str, **kwargs) -> "SpoonacularConfig":
        """Create config with explicit API key"""
        return cls(api_key=api_key, **kwargs)


class ClientDefaults:
    """Default values for the client"""
    
    BASE_URL = "https://api.spoonacular.com"
    TIMEOUT = 30
    RATE_LIMIT_DELAY = 0.1
    MAX_RETRIES = 3
    USER_AGENT = "SpoonacularPythonClient/2.0.0"
    
    # API Endpoints
    ENDPOINTS = {
        "recipes_complex_search": "/recipes/complexSearch",
        "recipes_find_by_ingredients": "/recipes/findByIngredients",
        "recipe_information": "/recipes/{id}/information",
        "recipe_nutrition": "/recipes/{id}/nutritionWidget.json",
        "recipe_ingredients": "/recipes/{id}/ingredientWidget.json",
        "recipe_equipment": "/recipes/{id}/equipmentWidget.json",
        "recipe_instructions": "/recipes/{id}/analyzedInstructions",
        "recipe_similar": "/recipes/{id}/similar",
        "recipes_random": "/recipes/random",
        "recipes_autocomplete": "/recipes/autocomplete",
    }