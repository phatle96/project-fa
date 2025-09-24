# Fresh Alert API Client

A comprehensive async Python client for the Fresh Alert API that provides food tracking, expiration monitoring, and product management capabilities.

## Features

- **Async/await support** with `httpx` for high-performance HTTP requests
- **Comprehensive error handling** with custom exception types
- **Automatic rate limiting** and request retries
- **Type-safe models** using Pydantic for request/response validation
- **Authentication support** for Bearer tokens and API keys
- **Configurable timeouts** and retry strategies
- **Context manager support** for proper resource management

## Installation

The client requires the following dependencies:
```bash
pip install httpx pydantic
```

## Quick Start

### Basic Usage

```python
import asyncio
from src.utils.freshalert import FreshAlertClient, FreshAlertConfig

async def main():
    # Bearer token passed as argument (typical LangGraph usage)
    bearer_token = "your-bearer-token-here"  # Usually from request headers
    config = FreshAlertConfig(bearer_token=bearer_token)
    
    async with FreshAlertClient(config) as client:
        # Get all user products
        products = await client.get_my_products()
        print(f"Found {len(products)} products")
        
        # Get products expiring in the next 7 days
        expiring = await client.get_expiring_products(days=7)
        print(f"Found {len(expiring)} expiring products")
        
        # Get already expired products
        expired = await client.get_expired_products()
        print(f"Found {len(expired)} expired products")

asyncio.run(main())
```

### Environment Variable Configuration (Optional)

For development or testing, you can optionally set environment variables:

```bash
export FRESH_ALERT_BASE_URL="https://api.freshalert.com"  # Optional base URL override
```

**Note:** In production LangGraph usage, the Bearer token should be passed as an argument from request headers rather than environment variables.

## API Endpoints

### Products API

The client currently supports these Fresh Alert API endpoints:

#### `GET /product/user`
Get all products for the current user.

```python
products = await client.get_my_products()
# OR
products = await client.products.get_user_products()
```

#### `GET /product/user/expired`
Get products that are expired or about to expire.

```python
# Get products expiring in next 7 days (default)
expiring = await client.get_expiring_products(days=7)

# Get already expired products
expired = await client.get_expired_products()

# Using the direct API
expired = await client.products.get_expired_products(days=3)
```

## Configuration

### FreshAlertConfig Options

```python
from src.utils.freshalert import FreshAlertConfig

config = FreshAlertConfig(
    # API Settings
    base_url="https://api.freshalert.com",    # API base URL
    api_version="v1",                         # API version
    
    # Authentication (choose one)
    bearer_token="your-bearer-token",         # Bearer token (recommended)
    api_key="your-api-key",                   # API key (alternative)
    
    # Request Settings
    timeout=30.0,                             # Request timeout in seconds
    max_retries=3,                            # Maximum retry attempts
    retry_delay=1.0,                          # Base delay between retries
    
    # Rate Limiting
    rate_limit=10.0                           # Max requests per second
)
```

### Environment Variables (Optional)

For development and testing purposes, you can optionally use environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FRESH_ALERT_BASE_URL` | Base URL for the API | `https://api.freshalert.com` |

**Note:** For production usage with LangGraph, Bearer tokens should be passed as arguments from request headers rather than environment variables for security.

## Error Handling

The client provides comprehensive error handling with specific exception types:

```python
from src.utils.freshalert import (
    FreshAlertClient,
    FreshAlertAuthenticationError,
    FreshAlertRateLimitError,
    FreshAlertNotFoundError,
    FreshAlertServerError
)

async with FreshAlertClient() as client:
    try:
        products = await client.get_my_products()
    except FreshAlertAuthenticationError:
        print("Authentication failed - check your token")
    except FreshAlertRateLimitError as e:
        print(f"Rate limit exceeded, retry after {e.retry_after} seconds")
    except FreshAlertNotFoundError:
        print("Resource not found")
    except FreshAlertServerError:
        print("Server error - try again later")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Exception Hierarchy

```
FreshAlertError (base)
├── FreshAlertAPIError
├── FreshAlertAuthenticationError (401)
├── FreshAlertAuthorizationError (403)
├── FreshAlertNotFoundError (404)
├── FreshAlertRateLimitError (429)
├── FreshAlertQuotaExceededError (429)
├── FreshAlertValidationError (400)
├── FreshAlertConnectionError
├── FreshAlertTimeoutError
└── FreshAlertServerError (5xx)
```

## Data Models

### ProductResponseDto

```python
class ProductResponseDto(BaseModel):
    id: str
    code_number: Optional[str]
    code_type: Optional[str]
    product_name: Optional[str]
    brand: Optional[str]
    manufacturer: Optional[str]
    description: Optional[str]
    image_url: Optional[List[str]]
    usage_instruction: Optional[str]
    storage_instruction: Optional[str]
    country_of_origin: Optional[str]
    category: Optional[str]
    nutrition_fact: Optional[str]
    label_key: Optional[str]
    phrase: Optional[str]
    date_product_users: Optional[List[DateResponseModel]]
```

### DateResponseModel

```python
class DateResponseModel(BaseModel):
    id: str
    product_id: str
    date_manufactured: Optional[datetime]
    date_best_before: Optional[datetime]
    date_expired: Optional[datetime]
    quantity: Optional[float]
```

## Advanced Usage

### Direct API Access

For more control, you can access the API modules directly:

```python
async with FreshAlertClient() as client:
    # Access products API directly
    products_api = client.products
    
    # Make direct API calls
    all_products = await products_api.get_user_products()
    expired_products = await products_api.get_expired_products(days=5)
    expiring_products = await products_api.get_expiring_products(days=7)
```

### Custom HTTP Client

For advanced use cases, you can access the underlying HTTP client:

```python
async with FreshAlertClient() as client:
    # Access the HTTP client directly
    http_client = client._http_client
    
    # Make custom requests
    response = await http_client.get("/custom/endpoint")
```

### Health Check

Check if the API is accessible and authentication works:

```python
async with FreshAlertClient() as client:
    try:
        is_healthy = await client.health_check()
        print(f"API health check: {'✓ PASS' if is_healthy else '✗ FAIL'}")
    except Exception as e:
        print(f"Health check failed: {e}")
```

## Integration with LangGraph

The Fresh Alert client is designed for seamless integration with LangGraph agents, where Bearer tokens are dynamically extracted from request headers:

```python
from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from src.utils.freshalert import FreshAlertClient, FreshAlertConfig

def get_auth_token(config: RunnableConfig) -> str | None:
    """Extract authentication token from request headers"""
    if not config:
        return None
    
    configurable = config.get("configurable", {})
    headers = configurable.get("headers", {})
    
    # Look for Authentication header from frontend
    auth_header = headers.get("Authentication") or headers.get("authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    
    return None

async def agent_function(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """Example agent function using Fresh Alert client"""
    
    # Get token from request headers (recommended approach)
    token = get_auth_token(config)
    if not token:
        raise ValueError("Authentication token is required")
    
    # Create Fresh Alert client with dynamic token
    fresh_alert_config = FreshAlertConfig(bearer_token=token)
    
    async with FreshAlertClient(fresh_alert_config) as client:
        # Get user's products
        products = await client.get_my_products()
        
        # Get expiring products
        expiring = await client.get_expiring_products(days=7)
        
        # Update state with results
        state["products"] = products
        state["expiring_products"] = expiring
    
    return state

# Alternative: Direct token passing
async def agent_with_direct_token(token: str, user_query: str) -> Dict[str, Any]:
    """Example with direct token passing"""
    
    config = FreshAlertConfig(bearer_token=token)
    
    async with FreshAlertClient(config) as client:
        # Perform operations based on user query
        if "expiring" in user_query.lower():
            products = await client.get_expiring_products(days=7)
        else:
            products = await client.get_my_products()
        
        return {"products": products, "query": user_query}
```

## Logging

The client uses Python's standard logging module. Enable debug logging to see detailed request/response information:

```python
import logging

# Enable debug logging for the Fresh Alert client
logging.getLogger("src.utils.freshalert").setLevel(logging.DEBUG)

# Or enable for all HTTP requests
logging.getLogger("httpx").setLevel(logging.DEBUG)
```

## Development

To extend the client with additional endpoints:

1. Add new models to `src/utils/freshalert/models/`
2. Create new API modules in `src/utils/freshalert/api/`
3. Add the new API to the main client in `src/utils/freshalert/client.py`
4. Update the `__init__.py` file to export new public classes

## License

This client is part of the Fresh Alert Agent project.