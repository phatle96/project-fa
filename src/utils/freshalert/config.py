"""
Configuration settings for Fresh Alert API client.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class FreshAlertConfig:
    """Configuration for Fresh Alert API client"""
    
    # API Settings
    base_url: str = "http://51.79.219.71:3000"  # Update with actual base URL
    api_version: str = "v1"
    
    # Authentication
    api_key: Optional[str] = None
    bearer_token: Optional[str] = None
    
    # Request settings
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Rate limiting (requests per second)
    rate_limit: float = 10.0
    
    def __post_init__(self):
        """Load configuration from environment variables as fallback if not provided"""
        # Note: For production LangGraph usage, bearer_token should be passed directly
        # Environment variables are only used as fallback for development/testing
        
        if self.api_key is None:
            self.api_key = os.getenv("FRESH_ALERT_API_KEY")
        
        if self.bearer_token is None:
            self.bearer_token = os.getenv("FRESH_ALERT_BEARER_TOKEN")
        
        if self.base_url == "http://51.79.219.71:3000":
            # Allow override from environment
            self.base_url = os.getenv("FRESH_ALERT_BASE_URL", self.base_url)
            
    def with_auth(self, bearer_token: Optional[str] = None, api_key: Optional[str] = None) -> dict:
        """Get auth headers with dynamic override"""
        headers = {}
        
        token = bearer_token or self.bearer_token
        key = api_key or self.api_key
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif key:
            headers["X-API-Key"] = key
        
        return headers
    
    @property
    def full_base_url(self) -> str:
        """Get the full base URL with API version"""
        return f"{self.base_url.rstrip('/')}/{self.api_version}"
    
    @property
    def auth_headers(self) -> dict:
        """Get authentication headers"""
        headers = {}
        
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key
        
        return headers


class ClientDefaults:
    """Default values for the client"""
    
    USER_AGENT = "FreshAlert-Python-Client/1.0.0"
    CONTENT_TYPE = "application/json"
    ACCEPT = "application/json"
    
    # Default timeouts
    CONNECTION_TIMEOUT = 10.0
    READ_TIMEOUT = 30.0
    
    # Default retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0
    BACKOFF_FACTOR = 2.0