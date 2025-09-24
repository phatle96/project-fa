"""
Custom exceptions for Spoonacular API client.
"""

from typing import Dict, Optional, Any


class SpoonacularError(Exception):
    """Base exception for all Spoonacular API errors"""
    pass


class SpoonacularAPIError(SpoonacularError):
    """Exception for API-specific errors with status codes"""
    
    def __init__(
        self, 
        status_code: int, 
        message: str, 
        response_data: Optional[Dict[str, Any]] = None,
        request_url: Optional[str] = None
    ):
        self.status_code = status_code
        self.message = message
        self.response_data = response_data or {}
        self.request_url = request_url
        
        super().__init__(f"API Error {status_code}: {message}")


class SpoonacularAuthenticationError(SpoonacularAPIError):
    """Exception for authentication/authorization errors (401, 403)"""
    pass


class SpoonacularRateLimitError(SpoonacularAPIError):
    """Exception for rate limit errors (429)"""
    
    def __init__(
        self, 
        retry_after: Optional[int] = None, 
        message: str = "Rate limit exceeded",
        **kwargs
    ):
        self.retry_after = retry_after
        super().__init__(status_code=429, message=message, **kwargs)


class SpoonacularQuotaExceededError(SpoonacularAPIError):
    """Exception for quota exceeded errors"""
    pass


class SpoonacularValidationError(SpoonacularError):
    """Exception for client-side validation errors"""
    pass


class SpoonacularConnectionError(SpoonacularError):
    """Exception for network/connection errors"""
    pass


class SpoonacularTimeoutError(SpoonacularError):
    """Exception for request timeout errors"""
    pass