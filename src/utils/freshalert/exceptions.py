"""
Exception classes for Fresh Alert API client.
"""

from typing import Optional, Dict, Any


class FreshAlertError(Exception):
    """Base exception for all Fresh Alert API errors"""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        self.error_code = error_code
        
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.status_code:
            return f"Fresh Alert API Error {self.status_code}: {self.message}"
        return f"Fresh Alert API Error: {self.message}"
    
    @property
    def is_client_error(self) -> bool:
        """Check if this is a 4xx client error"""
        return self.status_code is not None and 400 <= self.status_code < 500
    
    @property
    def is_server_error(self) -> bool:
        """Check if this is a 5xx server error"""
        return self.status_code is not None and 500 <= self.status_code < 600


class FreshAlertAPIError(FreshAlertError):
    """General API error from Fresh Alert service"""
    pass


class FreshAlertAuthenticationError(FreshAlertError):
    """Authentication failed - invalid or missing credentials"""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, status_code=401, **kwargs)


class FreshAlertAuthorizationError(FreshAlertError):
    """Authorization failed - insufficient permissions"""
    
    def __init__(self, message: str = "Insufficient permissions", **kwargs):
        super().__init__(message, status_code=403, **kwargs)


class FreshAlertNotFoundError(FreshAlertError):
    """Resource not found"""
    
    def __init__(self, message: str = "Resource not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class FreshAlertRateLimitError(FreshAlertError):
    """Rate limit exceeded"""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, status_code=429, **kwargs)
        self.retry_after = retry_after


class FreshAlertQuotaExceededError(FreshAlertError):
    """API quota exceeded"""
    
    def __init__(self, message: str = "API quota exceeded", **kwargs):
        super().__init__(message, status_code=429, **kwargs)


class FreshAlertValidationError(FreshAlertError):
    """Request validation failed"""
    
    def __init__(self, message: str = "Request validation failed", **kwargs):
        super().__init__(message, status_code=400, **kwargs)


class FreshAlertConnectionError(FreshAlertError):
    """Network connection error"""
    
    def __init__(self, message: str = "Connection error", **kwargs):
        super().__init__(message, **kwargs)


class FreshAlertTimeoutError(FreshAlertError):
    """Request timeout error"""
    
    def __init__(self, message: str = "Request timeout", **kwargs):
        super().__init__(message, **kwargs)


class FreshAlertServerError(FreshAlertError):
    """Internal server error (5xx)"""
    
    def __init__(self, message: str = "Internal server error", **kwargs):
        super().__init__(message, status_code=500, **kwargs)


def create_error_from_response(
    status_code: int,
    response_data: Dict[str, Any],
    default_message: str = "API request failed"
) -> FreshAlertError:
    """Create appropriate exception from HTTP response"""
    
    # Extract error message from response
    message = default_message
    error_code = None
    
    if isinstance(response_data, dict):
        # Try to extract error message from various possible fields
        message = (
            response_data.get("error") or
            response_data.get("message") or
            response_data.get("detail") or
            default_message
        )
        error_code = response_data.get("errorCode")
    
    # Create specific exception based on status code
    if status_code == 401:
        return FreshAlertAuthenticationError(message, response_data=response_data, error_code=error_code)
    elif status_code == 403:
        return FreshAlertAuthorizationError(message, response_data=response_data, error_code=error_code)
    elif status_code == 404:
        return FreshAlertNotFoundError(message, response_data=response_data, error_code=error_code)
    elif status_code == 429:
        # Check if it's rate limit or quota exceeded
        if "rate limit" in message.lower():
            return FreshAlertRateLimitError(message, response_data=response_data, error_code=error_code)
        else:
            return FreshAlertQuotaExceededError(message, response_data=response_data, error_code=error_code)
    elif status_code == 400:
        return FreshAlertValidationError(message, response_data=response_data, error_code=error_code)
    elif 500 <= status_code < 600:
        return FreshAlertServerError(message, status_code=status_code, response_data=response_data, error_code=error_code)
    else:
        return FreshAlertAPIError(message, status_code=status_code, response_data=response_data, error_code=error_code)