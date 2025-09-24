"""
Base HTTP client for Fresh Alert API with error handling and rate limiting.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin

import httpx

from .config import FreshAlertConfig, ClientDefaults
from .exceptions import (
    FreshAlertAPIError,
    FreshAlertAuthenticationError,
    FreshAlertRateLimitError,
    FreshAlertQuotaExceededError,
    FreshAlertConnectionError,
    FreshAlertTimeoutError,
    create_error_from_response
)

logger = logging.getLogger(__name__)


class BaseHttpClient:
    """Base HTTP client with error handling, rate limiting, and retries"""
    
    def __init__(self, config: FreshAlertConfig):
        self.config = config
        self._last_request_time = 0.0
        
        # Create HTTP client
        self.client = httpx.AsyncClient(
            timeout=config.timeout,
            headers={
                "User-Agent": ClientDefaults.USER_AGENT,
                "Accept": ClientDefaults.ACCEPT,
                "Content-Type": ClientDefaults.CONTENT_TYPE,
                **config.auth_headers
            }
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        """Close the HTTP client"""
        if self.client:
            await self.client.aclose()
    
    async def _rate_limit(self):
        """Implement rate limiting"""
        if self.config.rate_limit <= 0:
            return
            
        min_interval = 1.0 / self.config.rate_limit
        elapsed = time.time() - self._last_request_time
        
        if elapsed < min_interval:
            wait_time = min_interval - elapsed
            logger.debug(f"Rate limiting: waiting {wait_time:.2f} seconds")
            await asyncio.sleep(wait_time)
        
        self._last_request_time = time.time()
    
    async def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and convert errors to exceptions"""
        
        # Try to parse JSON response
        try:
            response_data = response.json()
        except Exception:
            response_data = {"error": response.text or "Unknown error"}
        
        # Check for successful status codes
        if response.is_success:
            return response_data
        
        # Handle error responses
        error = create_error_from_response(
            status_code=response.status_code,
            response_data=response_data,
            default_message=f"HTTP {response.status_code}: {response.reason_phrase}"
        )
        
        logger.error(f"API error: {error}")
        raise error
    
    async def _make_request_with_retries(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request with retries and error handling"""
        
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                # Rate limiting
                await self._rate_limit()
                
                # Make the request
                logger.debug(f"Making {method} request to {url} (attempt {attempt + 1})")
                response = await self.client.request(method, url, **kwargs)
                
                return await self._handle_response(response)
                
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                last_exception = FreshAlertConnectionError(f"Connection error: {str(e)}")
                
            except httpx.TimeoutException as e:
                last_exception = FreshAlertTimeoutError(f"Request timeout: {str(e)}")
                
            except FreshAlertRateLimitError as e:
                # For rate limit errors, respect retry-after if provided
                if hasattr(e, 'retry_after') and e.retry_after:
                    wait_time = e.retry_after
                else:
                    wait_time = self.config.retry_delay * (2 ** attempt)
                
                if attempt < self.config.max_retries:
                    logger.warning(f"Rate limit hit, retrying in {wait_time} seconds")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise e
                    
            except (FreshAlertAuthenticationError, FreshAlertQuotaExceededError) as e:
                # Don't retry authentication or quota errors
                raise e
                
            except FreshAlertAPIError as e:
                # For other API errors, only retry on server errors (5xx)
                if e.is_server_error and attempt < self.config.max_retries:
                    wait_time = self.config.retry_delay * (2 ** attempt)
                    logger.warning(f"Server error, retrying in {wait_time} seconds: {e}")
                    await asyncio.sleep(wait_time)
                    last_exception = e
                    continue
                else:
                    raise e
            
            except Exception as e:
                last_exception = FreshAlertAPIError(f"Unexpected error: {str(e)}")
            
            # If we get here, we had an error and should retry
            if attempt < self.config.max_retries:
                wait_time = self.config.retry_delay * (2 ** attempt)
                logger.warning(f"Request failed, retrying in {wait_time} seconds")
                await asyncio.sleep(wait_time)
        
        # If we exhausted all retries, raise the last exception
        if last_exception:
            raise last_exception
        else:
            raise FreshAlertAPIError("Request failed after all retry attempts")
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a GET request"""
        
        url = urljoin(self.config.full_base_url, endpoint.lstrip('/'))
        
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        return await self._make_request_with_retries(
            method="GET",
            url=url,
            params=params,
            headers=request_headers,
            **kwargs
        )
    
    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a POST request"""
        
        url = urljoin(self.config.full_base_url, endpoint.lstrip('/'))
        
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        return await self._make_request_with_retries(
            method="POST",
            url=url,
            data=data,
            json=json,
            params=params,
            headers=request_headers,
            **kwargs
        )
    
    async def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a PUT request"""
        
        url = urljoin(self.config.full_base_url, endpoint.lstrip('/'))
        
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        return await self._make_request_with_retries(
            method="PUT",
            url=url,
            data=data,
            json=json,
            params=params,
            headers=request_headers,
            **kwargs
        )
    
    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a DELETE request"""
        
        url = urljoin(self.config.full_base_url, endpoint.lstrip('/'))
        
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        return await self._make_request_with_retries(
            method="DELETE",
            url=url,
            params=params,
            headers=request_headers,
            **kwargs
        )