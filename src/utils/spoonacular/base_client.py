"""
Base HTTP client for Spoonacular API with error handling and rate limiting.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin

import httpx

from .config import SpoonacularConfig, ClientDefaults
from .exceptions import (
    SpoonacularAPIError,
    SpoonacularAuthenticationError, 
    SpoonacularRateLimitError,
    SpoonacularQuotaExceededError,
    SpoonacularConnectionError,
    SpoonacularTimeoutError
)

logger = logging.getLogger(__name__)


class BaseHttpClient:
    """Base HTTP client with error handling, rate limiting, and retries"""
    
    def __init__(self, config: SpoonacularConfig):
        self.config = config
        self._last_request_time = 0.0
        
        # Create HTTP client
        self.client = httpx.AsyncClient(
            timeout=config.timeout,
            headers={
                "User-Agent": ClientDefaults.USER_AGENT,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    def _build_url(self, endpoint: str, path_params: Optional[Dict[str, Any]] = None) -> str:
        """Build full URL with path parameter substitution"""
        url = endpoint
        
        # Substitute path parameters
        if path_params:
            for key, value in path_params.items():
                url = url.replace(f"{{{key}}}", str(value))
        
        return urljoin(self.config.base_url.rstrip('/') + '/', url.lstrip('/'))
    
    def _prepare_params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare query parameters for API request"""
        if params is None:
            params = {}
        
        # Remove None values
        clean_params = {k: v for k, v in params.items() if v is not None}
        
        # Add API key
        clean_params['apiKey'] = self.config.api_key
        
        # Convert values to appropriate string formats
        for key, value in clean_params.items():
            if isinstance(value, list):
                # Handle list of enums or regular values
                string_values = []
                for item in value:
                    if hasattr(item, 'value'):  # Enum
                        string_values.append(str(item.value))
                    else:
                        string_values.append(str(item))
                clean_params[key] = ','.join(string_values)
            elif isinstance(value, bool):
                clean_params[key] = str(value).lower()
            elif hasattr(value, 'value'):  # Single enum value
                clean_params[key] = str(value.value)
            else:
                clean_params[key] = str(value)
        
        return clean_params
    
    async def _rate_limit(self):
        """Apply rate limiting between requests"""
        if self.config.rate_limit_delay > 0:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.config.rate_limit_delay:
                await asyncio.sleep(self.config.rate_limit_delay - elapsed)
        
        self._last_request_time = time.time()
    
    def _handle_error_response(self, response: httpx.Response, request_url: str) -> None:
        """Handle error responses and raise appropriate exceptions"""
        status_code = response.status_code
        
        try:
            error_data = response.json()
            message = error_data.get('message', f'HTTP {status_code}')
        except Exception:
            error_data = {"error": response.text}
            message = f'HTTP {status_code}: {response.text[:100]}'
        
        # Handle specific error types
        if status_code == 401:
            raise SpoonacularAuthenticationError(
                status_code=status_code,
                message="Invalid API key or unauthorized access",
                response_data=error_data,
                request_url=request_url
            )
        elif status_code == 403:
            if "quota" in message.lower():
                raise SpoonacularQuotaExceededError(
                    status_code=status_code,
                    message=message,
                    response_data=error_data,
                    request_url=request_url
                )
            else:
                raise SpoonacularAuthenticationError(
                    status_code=status_code,
                    message=message,
                    response_data=error_data,
                    request_url=request_url
                )
        elif status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            raise SpoonacularRateLimitError(
                retry_after=retry_after,
                message=f"Rate limit exceeded. Retry after {retry_after} seconds",
                response_data=error_data,
                request_url=request_url
            )
        else:
            raise SpoonacularAPIError(
                status_code=status_code,
                message=message,
                response_data=error_data,
                request_url=request_url
            )
    
    async def _make_request_with_retries(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                await self._rate_limit()
                
                logger.debug(f"Making {method} request to {url} (attempt {attempt + 1})")
                
                response = await self.client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    **kwargs
                )
                
                # Handle success
                if 200 <= response.status_code < 300:
                    try:
                        return response.json()
                    except Exception as e:
                        raise SpoonacularAPIError(
                            status_code=response.status_code,
                            message=f"Failed to parse response JSON: {e}",
                            request_url=url
                        )
                
                # Handle errors
                self._handle_error_response(response, url)
                
            except SpoonacularRateLimitError as e:
                # For rate limits, wait and retry
                if attempt < self.config.max_retries:
                    wait_time = e.retry_after or 60
                    logger.warning(f"Rate limit hit, waiting {wait_time} seconds before retry {attempt + 1}")
                    await asyncio.sleep(wait_time)
                    last_exception = e
                    continue
                else:
                    raise e
                    
            except (SpoonacularAuthenticationError, SpoonacularQuotaExceededError) as e:
                # Don't retry auth or quota errors
                raise e
                
            except httpx.RequestError as e:
                last_exception = SpoonacularConnectionError(f"Request failed: {e}")
                if attempt < self.config.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Request failed, retrying in {wait_time} seconds: {e}")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise last_exception
                    
            except httpx.TimeoutException as e:
                last_exception = SpoonacularTimeoutError(f"Request timed out: {e}")
                if attempt < self.config.max_retries:
                    logger.warning(f"Request timed out, retrying: {e}")
                    await asyncio.sleep(1)
                    continue
                else:
                    raise last_exception
        
        # If we get here, all retries failed
        if last_exception:
            raise last_exception
        else:
            raise SpoonacularAPIError(
                status_code=500,
                message="All retry attempts failed",
                request_url=url
            )
    
    async def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a GET request"""
        url = self._build_url(endpoint, path_params)
        prepared_params = self._prepare_params(params)
        
        return await self._make_request_with_retries(
            method="GET",
            url=url,
            params=prepared_params
        )
    
    async def post(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a POST request"""
        url = self._build_url(endpoint, path_params)
        prepared_params = self._prepare_params(params)
        
        return await self._make_request_with_retries(
            method="POST",
            url=url,
            params=prepared_params,
            json=json_data
        )