"""
Fresh Alert API Python Client.

A comprehensive async Python client for the Fresh Alert API that provides
food tracking, expiration monitoring, and product management capabilities.

Example usage:
    >>> import asyncio
    >>> from freshalert import FreshAlertClient, FreshAlertConfig
    >>> 
    >>> async def main():
    >>>     config = FreshAlertConfig(bearer_token="your-token-here")
    >>>     
    >>>     async with FreshAlertClient(config) as client:
    >>>         # Get all user products
    >>>         products = await client.get_my_products()
    >>>         print(f"Found {len(products)} products")
    >>>         
    >>>         # Get products expiring in the next 7 days
    >>>         expiring = await client.get_expiring_products(days=7)
    >>>         print(f"Found {len(expiring)} expiring products")
    >>> 
    >>> asyncio.run(main())
"""

from .client import FreshAlertClient
from .config import FreshAlertConfig, ClientDefaults
from .exceptions import (
    FreshAlertError,
    FreshAlertAPIError,
    FreshAlertAuthenticationError,
    FreshAlertAuthorizationError,
    FreshAlertNotFoundError,
    FreshAlertRateLimitError,
    FreshAlertQuotaExceededError,
    FreshAlertValidationError,
    FreshAlertConnectionError,
    FreshAlertTimeoutError,
    FreshAlertServerError
)
from .models import (
    ResponseModel,
    DateResponseModel,
    ProductResponseDto,
    ProductListResponse,
    PaginatedProductData,
    PaginatedProductResponse,
    ProductSearchServiceResponse,
    IngredientDto,
    ProductFilterParams,
    CreateProductCodeRequest,
    CreateProductDateRequest,
    UpdateProductDateRequest,
    ProductCodeResponse,
    CreateProductCodeResponse,
    CreateProductDateResponse,
    UpdateProductDateResponse,
    DeleteProductResponse
)
from .api import ProductsAPI

# Version info
__version__ = "1.0.0"
__author__ = "Fresh Alert Team"
__email__ = "support@freshalert.com"

# Public API
__all__ = [
    # Main client
    "FreshAlertClient",
    
    # Configuration
    "FreshAlertConfig", 
    "ClientDefaults",
    
    # Exceptions
    "FreshAlertError",
    "FreshAlertAPIError", 
    "FreshAlertAuthenticationError",
    "FreshAlertAuthorizationError",
    "FreshAlertNotFoundError",
    "FreshAlertRateLimitError",
    "FreshAlertQuotaExceededError",
    "FreshAlertValidationError",
    "FreshAlertConnectionError",
    "FreshAlertTimeoutError",
    "FreshAlertServerError",
    
    # Models
    "ResponseModel",
    "DateResponseModel",
    "ProductResponseDto",
    "ProductListResponse",
    "PaginatedProductData",
    "PaginatedProductResponse",
    "ProductSearchServiceResponse",
    "IngredientDto",
    "ProductFilterParams",
    "CreateProductCodeRequest",
    "CreateProductDateRequest",
    "UpdateProductDateRequest",
    "ProductCodeResponse",
    "CreateProductCodeResponse",
    "CreateProductDateResponse",
    "UpdateProductDateResponse",
    "DeleteProductResponse",
    
    # API modules (for advanced usage)
    "ProductsAPI",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__"
]