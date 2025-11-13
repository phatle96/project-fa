"""
FreshAlert MCP Tools V2

This module provides improved MCP tools for Fresh Alert API interactions using
the generated Swagger client. Improvements over v1:

- Uses generated Swagger client for type safety and consistency
- Enhanced error handling with detailed error responses
- Better logging throughout all operations
- Consistent response structure across all tools
- Input validation with detailed error messages
- Proper datetime handling with ISO format conversion
- Clean separation of concerns
"""

import os
import sys
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timezone

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Add generated client to path
fresh_alert_api_dir = os.path.join(src_dir, "utils", "generate", "fresh_alert_api")
if fresh_alert_api_dir not in sys.path:
    sys.path.insert(0, fresh_alert_api_dir)

from utils.generate.fresh_alert_api.fresh_alert.client import AuthenticatedClient
from utils.generate.fresh_alert_api.fresh_alert import errors
from utils.generate.fresh_alert_api.fresh_alert.types import UNSET, Unset
from utils.generate.fresh_alert_api.fresh_alert.api.product import (
    product_controller_find_all_by_user,
    product_controller_find_all_by_user_lookback_days,
    product_controller_soft_delete_user_product_by_arr_product_ids,
)
from utils.generate.fresh_alert_api.fresh_alert.api.product_code import (
    barcode_controller_search,
    barcode_controller_create_product,
    barcode_controller_find_barcode_by_off,
)
from utils.generate.fresh_alert_api.fresh_alert.api.date import (
    date_controller_create,
    date_controller_update,
    date_controller_soft_delete_by_ids,
)

# Import models
from utils.generate.fresh_alert_api.fresh_alert.models import (
    CreateBarcodeInputDto,
    CreateDateProductUserDto,
    UpdateDateProductUserDto,
)

logger = logging.getLogger(__name__)


class FreshAlertToolsV2:
    """
    Improved MCP tools for Fresh Alert API interactions using generated Swagger client.
    
    Features:
    - Type-safe API calls using generated client
    - Comprehensive error handling
    - Detailed logging
    - Consistent response formatting
    - Input validation
    """
    
    def __init__(self, bearer_token: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Fresh Alert tools v2
        
        Args:
            bearer_token: Fresh Alert Bearer token (required for authentication)
            base_url: Base URL for Fresh Alert API (defaults to env variable or production URL)
        """
        self.bearer_token = bearer_token
        
        if not self.bearer_token:
            raise ValueError(
                "Fresh Alert Bearer token is required for authentication. "
                "Provide it via bearer_token parameter."
            )
        
        # Get base URL from env or use default
        self.base_url = base_url or os.getenv(
            "FRESH_ALERT_BASE_URL", 
            "http://51.79.219.71:3000/"
        )
        
        logger.info(f"Initialized FreshAlertToolsV2 with base_url: {self.base_url}")
    
    def _get_client(self) -> AuthenticatedClient:
        """
        Create an authenticated client for API calls.
        
        Returns:
            AuthenticatedClient configured with bearer token
        """
        return AuthenticatedClient(
            base_url=self.base_url,
            token=self.bearer_token,
            timeout=30.0,
            raise_on_unexpected_status=False,
        )
    
    def _format_error_response(
        self, 
        error_message: str, 
        error_type: str = "api_error",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Format a consistent error response.
        
        Args:
            error_message: Error message to return
            error_type: Type of error (api_error, validation_error, authentication_error, etc.)
            **kwargs: Additional context to include in response
            
        Returns:
            Formatted error dictionary
        """
        response = {
            "error": error_message,
            "error_type": error_type,
            **kwargs
        }
        return response
    
    def _serialize_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        """
        Serialize datetime to ISO format string.
        
        Args:
            dt: Datetime object to serialize
            
        Returns:
            ISO format string or None
        """
        if dt is None:
            return None
        return dt.isoformat()
    
    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """
        Parse ISO format string to datetime.
        
        Args:
            date_str: ISO format date string
            
        Returns:
            Datetime object or None
        """
        if not date_str:
            return None
        
        try:
            # Handle Z suffix for UTC
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            return datetime.fromisoformat(date_str)
        except ValueError as e:
            logger.error(f"Failed to parse datetime: {date_str}, error: {e}")
            raise ValueError(f"Invalid date format: {date_str}. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
    
    def _handle_unset(self, value: Any) -> Any:
        """
        Handle Unset values from the generated client.
        
        Args:
            value: Value that might be Unset
            
        Returns:
            None if Unset, otherwise the original value
        """
        if isinstance(value, Unset):
            return None
        return value
    
    async def get_user_products(self, is_expired: Optional[int] = None) -> Dict[str, Any]:
        """
        Get products for the current user with optional expiration filtering.
        
        This tool retrieves products associated with the authenticated user,
        including product details, expiration dates, and quantity information.
        
        Args:
            is_expired: Optional filter for product expiration status
                       - 1: Get only expired products
                       - -1: Get only non-expired products
                       - 0 or None: Get all products (expired and non-expired)
        
        Returns:
            Dictionary containing user's products and metadata
            
        Examples:
            # Get all user products (expired and non-expired)
            await get_user_products()
            
            # Get only non-expired products
            await get_user_products(is_expired=-1)
            
            # Get only expired products
            await get_user_products(is_expired=1)
            
            # Get all products explicitly
            await get_user_products(is_expired=0)
        """
        try:
            # Validate is_expired parameter
            if is_expired is not None and is_expired not in [1, -1, 0]:
                return self._format_error_response(
                    "is_expired parameter must be 1 (expired), -1 (non-expired), or 0 (all products)",
                    error_type="validation_error",
                    products=[]
                )
            
            # Convert to float for API call, or use UNSET
            api_is_expired = UNSET if is_expired is None else float(is_expired)
            
            async with self._get_client() as client:
                response = await product_controller_find_all_by_user.asyncio_detailed(
                    client=client,
                    is_expired=api_is_expired
                )
                
                if response.status_code == 404:
                    logger.info("No products found for user")
                    return {
                        "total_products": 0,
                        "products": [],
                        "message": "No products found for this user"
                    }
                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        products=[]
                    )
                
                if response.status_code != 200 or not response.parsed:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        products=[]
                    )
                
                products_data = response.parsed
                products_list = []
                
                # Parse and format product data
                if hasattr(products_data, 'data') and products_data.data:
                    for product in products_data.data:
                        product_dict = {
                            "id": self._handle_unset(getattr(product, 'id', None)),
                            "code_number": self._handle_unset(getattr(product, 'code_number', None)),
                            "code_type": self._handle_unset(getattr(product, 'code_type', None)),
                            "product_name": self._handle_unset(getattr(product, 'product_name', None)),
                            "brand": self._handle_unset(getattr(product, 'brand', None)),
                            "manufacturer": self._handle_unset(getattr(product, 'manufacturer', None)),
                            "description": self._handle_unset(getattr(product, 'description', None)),
                            "image_url": self._handle_unset(getattr(product, 'image_url', None)),
                            "usage_instruction": self._handle_unset(getattr(product, 'usage_instruction', None)),
                            "storage_instruction": self._handle_unset(getattr(product, 'storage_instruction', None)),
                            "country_of_origin": self._handle_unset(getattr(product, 'country_of_origin', None)),
                            "category": self._handle_unset(getattr(product, 'category', None)),
                            "nutrition_fact": self._handle_unset(getattr(product, 'nutrition_fact', None)),
                            "label_key": self._handle_unset(getattr(product, 'label_key', None)),
                            "phrase": self._handle_unset(getattr(product, 'phrase', None)),
                        }
                        
                        # Add date tracking information
                        date_tracking = []
                        if hasattr(product, 'date_product_users') and product.date_product_users:
                            for date_info in product.date_product_users:
                                date_dict = {
                                    "id": self._handle_unset(getattr(date_info, 'id', None)),
                                    "product_id": self._handle_unset(getattr(date_info, 'product_id', None)),
                                    "quantity": self._handle_unset(getattr(date_info, 'quantity', None)),
                                    "date_manufactured": self._serialize_datetime(self._handle_unset(getattr(date_info, 'date_manufactured', None))),
                                    "date_best_before": self._serialize_datetime(self._handle_unset(getattr(date_info, 'date_best_before', None))),
                                    "date_expired": self._serialize_datetime(self._handle_unset(getattr(date_info, 'date_expired', None))),
                                }
                                date_tracking.append(date_dict)
                        
                        product_dict["date_tracking"] = date_tracking
                        products_list.append(product_dict)
                
                logger.info(f"Retrieved {len(products_list)} products for user")
                return {
                    "total_products": len(products_list),
                    "products": products_list
                }
                
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                products=[]
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_user_products: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                products=[]
            )
    
    async def get_expired_products(self, days: int) -> Dict[str, Any]:
        """
        Get products that are about to expire for the current user.
        
        This tool retrieves products that will expire within a specified number of days.
        Useful for food waste prevention and meal planning based on expiring ingredients.
        
        Args:
            days: Number of days to look ahead for expiring products
            
        Returns:
            Dictionary containing expired/expiring products and metadata
            
        Examples:
            # Get products expiring in next 1 days
            await get_expired_products(days=1)
            
            # Get products expiring in next 3 days
            await get_expired_products(days=3)
        """
        try:
            # Input validation
            if days < 0:
                return self._format_error_response(
                    "Days parameter must be non-negative",
                    error_type="validation_error",
                    days=days,
                    products=[]
                )
            
            async with self._get_client() as client:
                response = await product_controller_find_all_by_user_lookback_days.asyncio_detailed(
                    client=client,
                    days=days
                )
                
                if response.status_code == 404:
                    logger.info(f"No expired products found for {days} days")
                    return {
                        "search_criteria": {
                            "days": days,
                            "description": f"products expiring within {days} days"
                        },
                        "total_products": 0,
                        "products": [],
                        "message": "No expired or expiring products found"
                    }
                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        search_criteria={"days": days},
                        products=[]
                    )
                
                if response.status_code != 200 or not response.parsed:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        search_criteria={"days": days},
                        products=[]
                    )
                
                products_data = response.parsed
                products_list = []
                
                # Parse and format product data with expiration details
                if hasattr(products_data, 'data') and products_data.data:
                    for product in products_data.data:
                        product_dict = {
                            "id": self._handle_unset(getattr(product, 'id', None)),
                            "code_number": self._handle_unset(getattr(product, 'code_number', None)),
                            "code_type": self._handle_unset(getattr(product, 'code_type', None)),
                            "product_name": self._handle_unset(getattr(product, 'product_name', None)),
                            "brand": self._handle_unset(getattr(product, 'brand', None)),
                            "manufacturer": self._handle_unset(getattr(product, 'manufacturer', None)),
                            "description": self._handle_unset(getattr(product, 'description', None)),
                            "image_url": self._handle_unset(getattr(product, 'image_url', None)),
                            "usage_instruction": self._handle_unset(getattr(product, 'usage_instruction', None)),
                            "storage_instruction": self._handle_unset(getattr(product, 'storage_instruction', None)),
                            "country_of_origin": self._handle_unset(getattr(product, 'country_of_origin', None)),
                            "category": self._handle_unset(getattr(product, 'category', None)),
                            "nutrition_fact": self._handle_unset(getattr(product, 'nutrition_fact', None)),
                            "label_key": self._handle_unset(getattr(product, 'label_key', None)),
                            "phrase": self._handle_unset(getattr(product, 'phrase', None)),
                        }
                        
                        # Add date tracking with expiration calculations
                        date_tracking = []
                        if hasattr(product, 'date_product_users') and product.date_product_users:
                            for date_info in product.date_product_users:
                                date_dict = {
                                    "id": self._handle_unset(getattr(date_info, 'id', None)),
                                    "product_id": self._handle_unset(getattr(date_info, 'product_id', None)),
                                    "quantity": self._handle_unset(getattr(date_info, 'quantity', None)),
                                    "date_manufactured": self._serialize_datetime(self._handle_unset(getattr(date_info, 'date_manufactured', None))),
                                    "date_best_before": self._serialize_datetime(self._handle_unset(getattr(date_info, 'date_best_before', None))),
                                    "date_expired": self._serialize_datetime(self._handle_unset(getattr(date_info, 'date_expired', None))),
                                }
                                
                                # Calculate days until expiration
                                date_expired = self._handle_unset(getattr(date_info, 'date_expired', None))
                                if date_expired:
                                    now = datetime.now(timezone.utc)
                                    if date_expired.tzinfo is None:
                                        date_expired = date_expired.replace(tzinfo=timezone.utc)
                                    
                                    days_until_expiry = (date_expired - now).days
                                    date_dict["days_until_expiry"] = days_until_expiry
                                    date_dict["is_expired"] = days_until_expiry < 0
                                    date_dict["expires_today"] = days_until_expiry == 0
                                
                                date_tracking.append(date_dict)
                        
                        product_dict["date_tracking"] = date_tracking
                        products_list.append(product_dict)
                
                logger.info(f"Retrieved {len(products_list)} products expiring within {days} days")
                return {
                    "search_criteria": {
                        "days": days,
                        "description": f"products expiring within {days} days"
                    },
                    "total_products": len(products_list),
                    "products": products_list
                }
                
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                search_criteria={"days": days},
                products=[]
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_expired_products: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                search_criteria={"days": days},
                products=[]
            )
    
    async def search_product_code(self, code: str) -> Dict[str, Any]:
        """
        Search for a product by its barcode/code number.
        
        This tool searches the Fresh Alert database for a product using its
        barcode or product code. Returns detailed product information if found.
        
        Args:
            code: The product barcode/code to search for (e.g., "1234567890123")
            
        Returns:
            Dictionary containing product information if found, or error message if not found
            
        Examples:
            # Search for a product by barcode
            await search_product_code(code="1234567890123")
        """
        try:
            # Input validation
            if not code or not code.strip():
                return self._format_error_response(
                    "Product code is required and cannot be empty",
                    error_type="validation_error",
                    found=False,
                    code=code,
                    product=None
                )
            
            async with self._get_client() as client:
                response = await barcode_controller_find_barcode_by_off.asyncio_detailed(
                    code=code.strip(),
                    client=client
                )
                
                if response.status_code == 404:
                    logger.info(f"No product found for code: {code}")
                    return {
                        "found": False,
                        "code": code,
                        "message": f"No product found for code: {code}",
                        "product": None
                    }
                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        found=False,
                        code=code,
                        product=None
                    )
                
                if response.status_code == 429:
                    logger.warning("Rate limit exceeded")
                    return self._format_error_response(
                        "Rate limit exceeded. Please try again later.",
                        error_type="rate_limit_error",
                        found=False,
                        code=code,
                        product=None
                    )
                
                if response.status_code != 200 or not response.parsed:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        found=False,
                        code=code,
                        product=None
                    )
                
                # Get the data from response
                response_data = response.parsed
                
                if not hasattr(response_data, 'data') or not response_data.data:
                    logger.info(f"No product data found for code: {code}")
                    return {
                        "found": False,
                        "code": code,
                        "message": f"No product found for code: {code}",
                        "product": None
                    }
                
                product_data = response_data.data
                
                # Format product information from BarcodeResponseModel
                product_dict = {
                    "id": self._handle_unset(getattr(product_data, 'id', None)),
                    "code_number": self._handle_unset(getattr(product_data, 'code_number', None)),
                    "code_type": self._handle_unset(getattr(product_data, 'code_type', None)),
                    "product_name": self._handle_unset(getattr(product_data, 'product_name', None)),
                    "brand": self._handle_unset(getattr(product_data, 'brand', None)),
                    "manufacturer": self._handle_unset(getattr(product_data, 'manufacturer', None)),
                    "description": self._handle_unset(getattr(product_data, 'description', None)),
                    "image_url": self._handle_unset(getattr(product_data, 'image_url', None)),
                    "usage_instruction": self._handle_unset(getattr(product_data, 'usage_instruction', None)),
                    "storage_instruction": self._handle_unset(getattr(product_data, 'storage_instruction', None)),
                    "country_of_origin": self._handle_unset(getattr(product_data, 'country_of_origin', None)),
                    "category": self._handle_unset(getattr(product_data, 'category', None)),
                    "nutrition_fact": self._handle_unset(getattr(product_data, 'nutrition_fact', None)),
                }
                
                # Add ingredients if available
                if hasattr(product_data, 'ingredients') and product_data.ingredients:
                    product_dict["ingredients"] = [
                        {
                            "id": self._handle_unset(getattr(ing, 'id', None)),
                            "name": self._handle_unset(getattr(ing, 'name', None)),
                            "description": self._handle_unset(getattr(ing, 'description', None)),
                            "origin_country": self._handle_unset(getattr(ing, 'origin_country', None)),
                            "is_allergen": self._handle_unset(getattr(ing, 'is_allergen', None)),
                        }
                        for ing in product_data.ingredients
                    ]
                else:
                    product_dict["ingredients"] = []
                
                logger.info(f"Found product for code: {code}")
                return {
                    "found": True,
                    "code": code,
                    "product": product_dict
                }
                
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                found=False,
                code=code,
                product=None
            )
        except Exception as e:
            logger.error(f"Unexpected error in search_product_code: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                found=False,
                code=code,
                product=None
            )
    
    async def create_product_code(
        self,
        code_number: str,
        code_type: Optional[str] = None,
        product_name: Optional[str] = None,
        brand: Optional[str] = None,
        manufacturer: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        country_of_origin: Optional[str] = None,
        usage_instruction: Optional[str] = None,
        storage_instruction: Optional[str] = None,
        image_url: Optional[List[str]] = None,
        nutrition_fact: Optional[str] = None,
        label_key: Optional[str] = None,
        phrase: Optional[str] = None,
        ingredients: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a new product code entry in the Fresh Alert database.
        
        This tool creates a new product with the specified information. The product
        can then be used to track expiration dates and quantities.
        
        Args:
            code_number: Product barcode/code number (required)
            code_type: Type of code (e.g., "UPC", "EAN", "Barcode")
            product_name: Name of the product
            brand: Product brand
            manufacturer: Product manufacturer
            description: Product description
            category: Product category (e.g., "Fruits", "Dairy")
            country_of_origin: Country where product originates
            usage_instruction: Instructions for product usage
            storage_instruction: Storage instructions
            image_url: List of product image URLs
            nutrition_fact: Nutrition facts information
            label_key: Label key
            phrase: Key phrase
            ingredients: List of ingredient dictionaries
            
        Returns:
            Dictionary containing created product information
            
        Examples:
            # Create a simple product
            await create_product_code(
                code_number="1234567890123",
                product_name="Organic Apples",
                brand="Fresh Farms"
            )
        """
        try:
            # Input validation
            if not code_number or not code_number.strip():
                return self._format_error_response(
                    "code_number is required and cannot be empty",
                    error_type="validation_error",
                    success=False,
                    product=None
                )
            
            # Build request body using generated model with camelCase keys
            body_dict = {
                "codeNumber": code_number,
            }
            
            # Add optional fields if provided (using camelCase)
            if code_type:
                body_dict["codeType"] = code_type
            if product_name:
                body_dict["productName"] = product_name
            if brand:
                body_dict["brand"] = brand
            if manufacturer:
                body_dict["manufacturer"] = manufacturer
            if description:
                body_dict["description"] = description
            if category:
                body_dict["category"] = category
            if country_of_origin:
                body_dict["countryOfOrigin"] = country_of_origin
            if usage_instruction:
                body_dict["usageInstruction"] = usage_instruction
            if storage_instruction:
                body_dict["storageInstruction"] = storage_instruction
            if image_url:
                body_dict["imageUrl"] = image_url
            if nutrition_fact:
                body_dict["nutritionFact"] = nutrition_fact
            if label_key:
                body_dict["labelKey"] = label_key
            if phrase:
                body_dict["phrase"] = phrase
            if ingredients:
                body_dict["ingredients"] = ingredients
            
            body = CreateBarcodeInputDto.from_dict(body_dict)
            
            async with self._get_client() as client:
                response = await barcode_controller_create_product.asyncio_detailed(
                    client=client,
                    body=body
                )
                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        success=False,
                        product=None
                    )
                
                if response.status_code == 404:
                    logger.error("Product creation endpoint not found")
                    return self._format_error_response(
                        "Product creation failed: endpoint not found",
                        error_type="api_error",
                        success=False,
                        product=None
                    )
                
                if response.status_code != 200 or not response.parsed:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        success=False,
                        product=None
                    )
                
                response_data = response.parsed
                
                # Check if we have data
                if hasattr(response_data, 'data') and response_data.data:
                    created_product = response_data.data
                    
                    # Format product data
                    product_dict = {
                        "id": self._handle_unset(getattr(created_product, 'id', None)),
                        "code_number": self._handle_unset(getattr(created_product, 'code_number', None)),
                        "code_type": self._handle_unset(getattr(created_product, 'code_type', None)),
                        "product_name": self._handle_unset(getattr(created_product, 'product_name', None)),
                        "brand": self._handle_unset(getattr(created_product, 'brand', None)),
                        "manufacturer": self._handle_unset(getattr(created_product, 'manufacturer', None)),
                        "description": self._handle_unset(getattr(created_product, 'description', None)),
                        "image_url": self._handle_unset(getattr(created_product, 'image_url', None)),
                        "usage_instruction": self._handle_unset(getattr(created_product, 'usage_instruction', None)),
                        "storage_instruction": self._handle_unset(getattr(created_product, 'storage_instruction', None)),
                        "country_of_origin": self._handle_unset(getattr(created_product, 'country_of_origin', None)),
                        "category": self._handle_unset(getattr(created_product, 'category', None)),
                        "nutrition_fact": self._handle_unset(getattr(created_product, 'nutrition_fact', None)),
                    }
                else:
                    # Fallback if no data wrapper
                    product_dict = {}
                
                logger.info(f"Created product with code: {code_number}")
                return {
                    "success": True,
                    "message": f"Successfully created product: {product_name or code_number}",
                    "product": product_dict
                }
                
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return self._format_error_response(
                f"Validation error: {str(e)}",
                error_type="validation_error",
                success=False,
                product=None
            )
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                success=False,
                product=None
            )
        except Exception as e:
            logger.error(f"Unexpected error in create_product_code: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                success=False,
                product=None
            )
    
    async def create_product_date(
        self,
        product_id: str,
        date_manufactured: Optional[str] = None,
        date_best_before: Optional[str] = None,
        date_expired: Optional[str] = None,
        quantity: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Create a new product date entry for tracking expiration and other important dates.
        
        This tool adds date tracking information to an existing product. Use this to
        track manufacturing dates, best before dates, expiration dates, and quantities.
        
        Args:
            product_id: ID of the product to add date information to (required)
            date_manufactured: Manufacturing date in ISO format (e.g., "2024-01-15T10:30:00")
            date_best_before: Best before date in ISO format
            date_expired: Expiration date in ISO format
            quantity: Quantity of the product (e.g., 2.5 for 2.5 kg)
            
        Returns:
            Dictionary containing created date entry information
            
        Examples:
            # Add expiration tracking to a product
            await create_product_date(
                product_id="12345678-1234-1234-1234-123456789012",
                date_expired="2024-12-31T23:59:59",
                quantity=1.0
            )
        """
        try:
            # Input validation
            if not product_id or not product_id.strip():
                return self._format_error_response(
                    "product_id is required and cannot be empty",
                    error_type="validation_error",
                    success=False,
                    product_id=product_id,
                    date_entry=None
                )
            
            # Build request body with camelCase keys and string date values
            body_dict = {
                "productId": product_id,
            }
            
            # Pass raw date strings (the model will parse them internally)
            if date_manufactured:
                body_dict["dateManufactured"] = date_manufactured
            if date_best_before:
                body_dict["dateBestBefore"] = date_best_before
            if date_expired:
                body_dict["dateExpired"] = date_expired
            if quantity is not None:
                body_dict["quantity"] = quantity
            
            body = CreateDateProductUserDto.from_dict(body_dict)
            
            async with self._get_client() as client:
                response = await date_controller_create.asyncio_detailed(
                    client=client,
                    body=body
                )
                
                print("parsed response: ", response.parsed)

                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        success=False,
                        product_id=product_id,
                        date_entry=None
                    )
                
                if response.status_code == 404:
                    logger.error(f"Product not found: {product_id}")
                    return self._format_error_response(
                        f"Product not found with ID: {product_id}",
                        error_type="not_found_error",
                        success=False,
                        product_id=product_id,
                        date_entry=None
                    )
                
                if response.status_code not in [200, 201] or not response.parsed:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        success=False,
                        product_id=product_id,
                        date_entry=None
                    )
                
                response_data = response.parsed

                
                # Check if we have data
                if hasattr(response_data, 'data') and response_data.data:
                    created_date = response_data.data
                else:
                    # Fallback to direct response
                    created_date = response_data
                
                # Format date entry
                date_dict = {
                    "id": self._handle_unset(getattr(created_date, 'id', None)),
                    "product_id": self._handle_unset(getattr(created_date, 'product_id', None)),
                    "quantity": self._handle_unset(getattr(created_date, 'quantity', None)),
                    "date_manufactured": self._serialize_datetime(self._handle_unset(getattr(created_date, 'date_manufactured', None))),
                    "date_best_before": self._serialize_datetime(self._handle_unset(getattr(created_date, 'date_best_before', None))),
                    "date_expired": self._serialize_datetime(self._handle_unset(getattr(created_date, 'date_expired', None))),
                }
                
                logger.info(f"Created date entry for product: {product_id}")
                return {
                    "success": True,
                    "message": f"Successfully created date tracking for product: {product_id}",
                    "product_id": product_id,
                    "date_entry": date_dict
                }
                
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return self._format_error_response(
                str(e),
                error_type="validation_error",
                success=False,
                product_id=product_id,
                date_entry=None
            )
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                success=False,
                product_id=product_id,
                date_entry=None
            )
        except Exception as e:
            logger.error(f"Unexpected error in create_product_date: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                success=False,
                product_id=product_id,
                date_entry=None
            )
    
    async def search_product_by_name(self, query: str) -> Dict[str, Any]:
        """
        Search for products by name or query string.
        
        This tool searches the Fresh Alert database for products matching
        the provided query string. Useful for finding products by name.
        
        Args:
            query: Search query string (product name or partial name)
            
        Returns:
            Dictionary containing list of matching products
            
        Examples:
            # Search for products by name
            await search_product_by_name(query="apple")
        """
        try:
            # Input validation
            if not query or not query.strip():
                return self._format_error_response(
                    "Search query is required and cannot be empty",
                    error_type="validation_error",
                    query=query,
                    products=[]
                )
            
            async with self._get_client() as client:
                response = await barcode_controller_search.asyncio_detailed(
                    query=query.strip(),
                    client=client
                )
                
                if response.status_code == 404:
                    logger.info(f"No products found for query: {query}")
                    return {
                        "total_products": 0,
                        "query": query,
                        "products": [],
                        "message": f"No products found matching: {query}"
                    }
                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        query=query,
                        products=[]
                    )
                
                if response.status_code == 429:
                    logger.warning("Rate limit exceeded")
                    return self._format_error_response(
                        "Rate limit exceeded. Please try again later.",
                        error_type="rate_limit_error",
                        query=query,
                        products=[]
                    )
                
                if response.status_code != 200 or not response.parsed:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        query=query,
                        products=[]
                    )
                
                # Get the data from response
                response_data = response.parsed
                
                if not hasattr(response_data, 'data') or not response_data.data:
                    logger.info(f"No products found for query: {query}")
                    return {
                        "total_products": 0,
                        "query": query,
                        "products": [],
                        "message": f"No products found matching: {query}"
                    }
                
                search_result = response_data.data
                
                # Check if products exist in the search result
                if not hasattr(search_result, 'products') or not search_result.products:
                    logger.info(f"No products in search results for query: {query}")
                    return {
                        "total_products": 0,
                        "query": query,
                        "products": [],
                        "message": f"No products found matching: {query}"
                    }
                
                # Format products list from OpenFoodSearchResultDto
                products_list = []
                for product in search_result.products:
                    product_dict = {
                        "code": self._handle_unset(getattr(product, 'code', None)),
                        "product_name": self._handle_unset(getattr(product, 'product_name', None)),
                        "brands": self._handle_unset(getattr(product, 'brands', None)),
                        "image_url": self._handle_unset(getattr(product, 'image_url', None)),
                    }
                    products_list.append(product_dict)
                
                logger.info(f"Found {len(products_list)} products matching query: {query}")
                return {
                    "total_products": len(products_list),
                    "query": query,
                    "products": products_list
                }
                
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                query=query,
                products=[]
            )
        except Exception as e:
            logger.error(f"Unexpected error in search_product_by_name: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                query=query,
                products=[]
            )
    
    async def update_product_date(
        self,
        date_id: str,
        product_id: str,
        date_manufactured: Optional[str] = None,
        date_best_before: Optional[str] = None,
        date_expired: Optional[str] = None,
        quantity: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Update an existing product date entry.
        
        This tool updates date tracking information for an existing product date entry.
        Use this to modify manufacturing dates, best before dates, expiration dates, or quantities.
        
        Args:
            date_id: ID of the date entry to update (required)
            product_id: ID of the product that linked to the date_id
            date_manufactured: Manufacturing date in ISO format (e.g., "2024-01-15T10:30:00")
            date_best_before: Best before date in ISO format
            date_expired: Expiration date in ISO format
            quantity: Quantity of the product (e.g., 2.5 for 2.5 kg)
            
        Returns:
            Dictionary containing updated date entry information
            
        Examples:
            # Update expiration date of an entry
            await update_product_date(
                product_id="a60e2e75-5ae3-4679-90de-7c7d29b24d56"
                date_id="12345678-1234-1234-1234-123456789012",
                date_expired="2024-12-31T23:59:59",
                quantity=0.5
            )
        """
        try:
            # Input validation
            if not date_id or not date_id.strip():
                return self._format_error_response(
                    "date_id is required and cannot be empty",
                    error_type="validation_error",
                    success=False,
                    date_id=date_id,
                    date_entry=None
                )
            
            if not product_id or not product_id.strip():
                return self._format_error_response(
                    "product_id is required and cannot be empty",
                    error_type="validation_error",
                    success=False,
                    date_id=date_id,
                    date_entry=None
                )
            
            # Build request body with camelCase keys and string date values
            body_dict = {
                "productId": product_id,
            }
            
            # Pass raw date strings (the model will parse them internally)
            if date_manufactured:
                body_dict["dateManufactured"] = date_manufactured
            if date_best_before:
                body_dict["dateBestBefore"] = date_best_before
            if date_expired:
                body_dict["dateExpired"] = date_expired
            if quantity is not None:
                body_dict["quantity"] = quantity
            
            body = UpdateDateProductUserDto.from_dict(body_dict)
            
            async with self._get_client() as client:
                response = await date_controller_update.asyncio_detailed(
                    id=date_id,
                    client=client,
                    body=body
                )
                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        success=False,
                        date_id=date_id,
                        date_entry=None
                    )
                
                if response.status_code == 404:
                    logger.error(f"Date entry not found: {date_id}")
                    return self._format_error_response(
                        f"Date entry not found with ID: {date_id}",
                        error_type="not_found_error",
                        success=False,
                        date_id=date_id,
                        date_entry=None
                    )
                
                if response.status_code != 200 or not response.parsed:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        success=False,
                        date_id=date_id,
                        date_entry=None
                    )
                
                response_data = response.parsed
                
                # Check if we have data
                if hasattr(response_data, 'data') and response_data.data:
                    updated_date = response_data.data
                else:
                    # Fallback to direct response
                    updated_date = response_data
                
                # Format date entry
                date_dict = {
                    "id": self._handle_unset(getattr(updated_date, 'id', None)),
                    "product_id": self._handle_unset(getattr(updated_date, 'product_id', None)),
                    "quantity": self._handle_unset(getattr(updated_date, 'quantity', None)),
                    "date_manufactured": self._serialize_datetime(self._handle_unset(getattr(updated_date, 'date_manufactured', None))),
                    "date_best_before": self._serialize_datetime(self._handle_unset(getattr(updated_date, 'date_best_before', None))),
                    "date_expired": self._serialize_datetime(self._handle_unset(getattr(updated_date, 'date_expired', None))),
                }
                
                logger.info(f"Updated date entry: {date_id}")
                return {
                    "success": True,
                    "message": f"Successfully updated date tracking entry: {date_id}",
                    "date_id": date_id,
                    "date_entry": date_dict
                }
                
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return self._format_error_response(
                str(e),
                error_type="validation_error",
                success=False,
                date_id=date_id,
                date_entry=None
            )
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                success=False,
                date_id=date_id,
                date_entry=None
            )
        except Exception as e:
            logger.error(f"Unexpected error in update_product_date: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                success=False,
                date_id=date_id,
                date_entry=None
            )
    
    async def delete_product_date(self, date_ids: List[str]) -> Dict[str, Any]:
        """
        Soft delete product date entries by their IDs.
        
        This tool soft deletes one or more product date entries (date tracking records),
        removing them from active tracking while preserving the data for audit purposes.
        
        Args:
            date_ids: List of date entry IDs to delete (required, must be non-empty)
            
        Returns:
            Dictionary containing deletion confirmation
            
        Examples:
            # Delete a single date entry
            await delete_product_date(date_ids=["12345678-1234-1234-1234-123456789012"])
            
            # Delete multiple date entries
            await delete_product_date(date_ids=[
                "12345678-1234-1234-1234-123456789012",
                "87654321-4321-4321-4321-210987654321"
            ])
        """
        try:
            # Input validation
            if not date_ids or not isinstance(date_ids, list):
                return self._format_error_response(
                    "date_ids is required and must be a list",
                    error_type="validation_error",
                    success=False,
                    date_ids=date_ids
                )
            
            if len(date_ids) == 0:
                return self._format_error_response(
                    "date_ids list cannot be empty",
                    error_type="validation_error",
                    success=False,
                    date_ids=date_ids
                )
            
            # Validate each ID
            for date_id in date_ids:
                if not date_id or not isinstance(date_id, str) or not date_id.strip():
                    return self._format_error_response(
                        f"Invalid date_id in list: {date_id}. All IDs must be non-empty strings.",
                        error_type="validation_error",
                        success=False,
                        date_ids=date_ids
                    )
            
            # Strip whitespace from all IDs
            cleaned_ids = [date_id.strip() for date_id in date_ids]
            
            async with self._get_client() as client:
                response = await date_controller_soft_delete_by_ids.asyncio_detailed(
                    client=client,
                    body=cleaned_ids
                )
                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        success=False,
                        date_ids=date_ids
                    )
                
                if response.status_code == 404:
                    logger.error(f"One or more date entries not found: {date_ids}")
                    return self._format_error_response(
                        f"One or more date entries not found with provided IDs",
                        error_type="not_found_error",
                        success=False,
                        date_ids=date_ids
                    )
                
                if response.status_code != 200:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        success=False,
                        date_ids=date_ids
                    )
                
                logger.info(f"Deleted {len(date_ids)} date entries: {date_ids}")
                return {
                    "success": True,
                    "message": f"Successfully deleted {len(date_ids)} date entry/entries",
                    "deleted_count": len(date_ids),
                    "date_ids": date_ids
                }
                
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                success=False,
                date_ids=date_ids
            )
        except Exception as e:
            logger.error(f"Unexpected error in delete_product_date: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                success=False,
                date_ids=date_ids
            )
    
    async def delete_product(self, product_ids: List[str]) -> Dict[str, Any]:
        """
        Soft delete products from the user's list.
        
        This tool soft deletes one or more products, removing them from the user's active 
        product list while preserving the data for potential recovery or audit purposes.
        
        Args:
            product_ids: List of product IDs to delete (required, must be non-empty)
            
        Returns:
            Dictionary containing deletion confirmation
            
        Examples:
            # Delete a single product
            await delete_product(product_ids=["12345678-1234-1234-1234-123456789012"])
            
            # Delete multiple products
            await delete_product(product_ids=[
                "12345678-1234-1234-1234-123456789012",
                "87654321-4321-4321-4321-210987654321"
            ])
        """
        try:
            # Input validation
            if not product_ids or not isinstance(product_ids, list):
                return self._format_error_response(
                    "product_ids is required and must be a list",
                    error_type="validation_error",
                    success=False,
                    product_ids=product_ids
                )
            
            if len(product_ids) == 0:
                return self._format_error_response(
                    "product_ids list cannot be empty",
                    error_type="validation_error",
                    success=False,
                    product_ids=product_ids
                )
            
            # Validate each ID
            for product_id in product_ids:
                if not product_id or not isinstance(product_id, str) or not product_id.strip():
                    return self._format_error_response(
                        f"Invalid product_id in list: {product_id}. All IDs must be non-empty strings.",
                        error_type="validation_error",
                        success=False,
                        product_ids=product_ids
                    )
            
            # Strip whitespace from all IDs
            cleaned_ids = [product_id.strip() for product_id in product_ids]
            
            async with self._get_client() as client:
                response = await product_controller_soft_delete_user_product_by_arr_product_ids.asyncio_detailed(
                    client=client,
                    body=cleaned_ids
                )
                
                if response.status_code == 401:
                    logger.error("Authentication failed")
                    return self._format_error_response(
                        "Authentication failed. Please check your Bearer token.",
                        error_type="authentication_error",
                        success=False,
                        product_ids=product_ids
                    )
                
                if response.status_code == 404:
                    logger.error(f"One or more products not found: {product_ids}")
                    return self._format_error_response(
                        f"One or more products not found with provided IDs",
                        error_type="not_found_error",
                        success=False,
                        product_ids=product_ids
                    )
                
                if response.status_code != 200:
                    logger.error(f"API returned status {response.status_code}")
                    return self._format_error_response(
                        f"API error: Received status code {response.status_code}",
                        error_type="api_error",
                        status_code=response.status_code,
                        success=False,
                        product_ids=product_ids
                    )
                
                logger.info(f"Deleted {len(product_ids)} products: {product_ids}")
                return {
                    "success": True,
                    "message": f"Successfully deleted {len(product_ids)} product(s)",
                    "deleted_count": len(product_ids),
                    "product_ids": product_ids
                }
                
        except errors.UnexpectedStatus as e:
            logger.error(f"Unexpected API status: {e}")
            return self._format_error_response(
                f"Unexpected API response: {str(e)}",
                error_type="api_error",
                success=False,
                product_ids=product_ids
            )
        except Exception as e:
            logger.error(f"Unexpected error in delete_product: {e}", exc_info=True)
            return self._format_error_response(
                f"Unexpected error: {str(e)}",
                error_type="unexpected_error",
                success=False,
                product_ids=product_ids
            )
