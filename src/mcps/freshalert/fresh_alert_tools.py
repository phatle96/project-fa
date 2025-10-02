import asyncio
import os
import sys
from typing import List, Optional, Dict, Any, Union
import logging

# Add the src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from utils.freshalert import (
    FreshAlertClient,
    FreshAlertConfig,
    ProductResponseDto,
    CreateProductCodeRequest,
    CreateProductDateRequest,
    FreshAlertError,
    FreshAlertAuthenticationError,
    FreshAlertNotFoundError
)

logger = logging.getLogger(__name__)

class FreshAlertTools:
    """MCP tools for Fresh Alert API interactions"""
    
    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialize Fresh Alert tools
        
        Args:
            bearer_token: Fresh Alert Bearer token (required for authentication)
        """
        self.bearer_token = bearer_token
        
        if not self.bearer_token:
            raise ValueError(
                "Fresh Alert Bearer token is required. "
            )
    
    async def get_user_products(self) -> Dict[str, Any]:
        """
        Get all products for the current user.
        
        This tool retrieves all products associated with the authenticated user,
        including product details, expiration dates, and quantity information.
        
        Returns:
            Dictionary containing user's products and metadata
            
        Examples:
            # Get all user products
            await get_user_products()
        """
        try:
            config = FreshAlertConfig(bearer_token=self.bearer_token)
            
            async with FreshAlertClient(config) as client:
                products = await client.get_my_products()
                
                # Convert to dictionary for MCP response
                response_data = {
                    "total_products": len(products),
                    "products": []
                }
                
                for product in products:
                    product_data = {
                        "id": product.id,
                        "code_number": product.code_number,
                        "code_type": product.code_type,
                        "product_name": product.product_name,
                        "brand": product.brand,
                        "manufacturer": product.manufacturer,
                        "description": product.description,
                        "image_url": product.image_url,
                        "usage_instruction": product.usage_instruction,
                        "storage_instruction": product.storage_instruction,
                        "country_of_origin": product.country_of_origin,
                        "category": product.category,
                        "nutrition_fact": product.nutrition_fact,
                        "label_key": product.label_key,
                        "phrase": product.phrase
                    }
                    
                    # Add date tracking information
                    if product.date_product_users:
                        product_data["date_tracking"] = []
                        for date_info in product.date_product_users:
                            date_data = {
                                "id": date_info.id,
                                "product_id": date_info.product_id,
                                "quantity": date_info.quantity
                            }
                            
                            # Convert datetime objects to ISO strings for JSON serialization
                            if date_info.date_manufactured:
                                date_data["date_manufactured"] = date_info.date_manufactured.isoformat()
                            if date_info.date_best_before:
                                date_data["date_best_before"] = date_info.date_best_before.isoformat()
                            if date_info.date_expired:
                                date_data["date_expired"] = date_info.date_expired.isoformat()
                            
                            product_data["date_tracking"].append(date_data)
                    else:
                        product_data["date_tracking"] = []
                    
                    response_data["products"].append(product_data)
                
                logger.info(f"Retrieved {len(products)} products for user")
                return response_data
                
        except FreshAlertAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "error": "Authentication failed. Please check your Bearer token.",
                "error_type": "authentication_error",
                "products": []
            }
        except FreshAlertNotFoundError as e:
            logger.warning(f"No products found: {e}")
            return {
                "total_products": 0,
                "products": [],
                "message": "No products found for this user"
            }
        except FreshAlertError as e:
            logger.error(f"Fresh Alert API error: {e}")
            return {
                "error": f"Fresh Alert API error: {str(e)}",
                "error_type": "api_error",
                "error_code": getattr(e, 'error_code', None),
                "products": []
            }
        except Exception as e:
            logger.error(f"Unexpected error in get_user_products: {e}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "products": []
            }
    
    async def get_expired_products(self, days: Optional[int] = None) -> Dict[str, Any]:
        """
        Get products that are expired or about to expire for the current user.
        
        This tool retrieves products that have expired or will expire within
        a specified number of days. Useful for food waste prevention and
        meal planning based on expiring ingredients.
        
        Args:
            days: Number of days to look ahead for expiring products (optional)
                 If None, returns already expired products
                 If positive integer, returns products expiring within that many days
        
        Returns:
            Dictionary containing expired/expiring products and metadata
            
        Examples:
            # Get already expired products
            await get_expired_products()
            
            # Get products expiring in next 7 days
            await get_expired_products(days=7)
            
            # Get products expiring in next 3 days
            await get_expired_products(days=3)
        """
        try:
            config = FreshAlertConfig(bearer_token=self.bearer_token)
            
            async with FreshAlertClient(config) as client:
                if days is None:
                    # Get already expired products
                    products = await client.get_expired_products()
                    search_description = "expired products"
                else:
                    # Get products expiring within specified days
                    products = await client.get_expiring_products(days=days)
                    search_description = f"products expiring within {days} days"
                
                # Convert to dictionary for MCP response
                response_data = {
                    "search_criteria": {
                        "days": days,
                        "description": search_description
                    },
                    "total_products": len(products),
                    "products": []
                }
                
                for product in products:
                    product_data = {
                        "id": product.id,
                        "code_number": product.code_number,
                        "code_type": product.code_type,
                        "product_name": product.product_name,
                        "brand": product.brand,
                        "manufacturer": product.manufacturer,
                        "description": product.description,
                        "image_url": product.image_url,
                        "usage_instruction": product.usage_instruction,
                        "storage_instruction": product.storage_instruction,
                        "country_of_origin": product.country_of_origin,
                        "category": product.category,
                        "nutrition_fact": product.nutrition_fact,
                        "label_key": product.label_key,
                        "phrase": product.phrase
                    }
                    
                    # Add date tracking information with expiration details
                    if product.date_product_users:
                        product_data["date_tracking"] = []
                        for date_info in product.date_product_users:
                            date_data = {
                                "id": date_info.id,
                                "product_id": date_info.product_id,
                                "quantity": date_info.quantity
                            }
                            
                            # Convert datetime objects to ISO strings
                            if date_info.date_manufactured:
                                date_data["date_manufactured"] = date_info.date_manufactured.isoformat()
                            if date_info.date_best_before:
                                date_data["date_best_before"] = date_info.date_best_before.isoformat()
                            if date_info.date_expired:
                                date_data["date_expired"] = date_info.date_expired.isoformat()
                                
                                # Calculate days until expiration (if expired, will be negative)
                                from datetime import datetime, timezone
                                now = datetime.now(timezone.utc)
                                expiry_date = date_info.date_expired
                                if expiry_date.tzinfo is None:
                                    # Assume UTC if no timezone info
                                    expiry_date = expiry_date.replace(tzinfo=timezone.utc)
                                
                                days_until_expiry = (expiry_date - now).days
                                date_data["days_until_expiry"] = days_until_expiry
                                date_data["is_expired"] = days_until_expiry < 0
                                date_data["expires_today"] = days_until_expiry == 0
                            
                            product_data["date_tracking"].append(date_data)
                    else:
                        product_data["date_tracking"] = []
                    
                    response_data["products"].append(product_data)
                
                logger.info(f"Retrieved {len(products)} {search_description}")
                return response_data
                
        except FreshAlertAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "error": "Authentication failed. Please check your Bearer token.",
                "error_type": "authentication_error",
                "search_criteria": {"days": days},
                "products": []
            }
        except FreshAlertNotFoundError as e:
            logger.warning(f"No expired products found: {e}")
            return {
                "search_criteria": {
                    "days": days,
                    "description": f"products expiring within {days} days" if days else "expired products"
                },
                "total_products": 0,
                "products": [],
                "message": "No expired or expiring products found"
            }
        except FreshAlertError as e:
            logger.error(f"Fresh Alert API error: {e}")
            return {
                "error": f"Fresh Alert API error: {str(e)}",
                "error_type": "api_error",
                "error_code": getattr(e, 'error_code', None),
                "search_criteria": {"days": days},
                "products": []
            }
        except Exception as e:
            logger.error(f"Unexpected error in get_expired_products: {e}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "search_criteria": {"days": days},
                "products": []
            }

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
            await search_product_code("1234567890123")
        """
        try:
            config = FreshAlertConfig(bearer_token=self.bearer_token)
            
            async with FreshAlertClient(config) as client:
                product = await client.products.search_product_code(code)
                
                if not product:
                    return {
                        "found": False,
                        "code": code,
                        "message": f"No product found for code: {code}",
                        "product": None
                    }
                
                # Convert product to dictionary
                product_data = {
                    "id": product.id,
                    "code_number": product.code_number,
                    "code_type": product.code_type,
                    "product_name": product.product_name,
                    "brand": product.brand,
                    "manufacturer": product.manufacturer,
                    "description": product.description,
                    "image_url": product.image_url,
                    "usage_instruction": product.usage_instruction,
                    "storage_instruction": product.storage_instruction,
                    "country_of_origin": product.country_of_origin,
                    "category": product.category,
                    "nutrition_fact": product.nutrition_fact,
                    "label_key": product.label_key,
                    "phrase": product.phrase
                }
                
                # Add ingredients if available
                if product.ingredients:
                    product_data["ingredients"] = [
                        {
                            "id": ing.id,
                            "off_id": ing.off_id,
                            "name": ing.name,
                            "description": ing.description,
                            "origin_country": ing.origin_country,
                            "is_allergen": ing.is_allergen,
                            "date_created": ing.date_created.isoformat() if ing.date_created else None
                        }
                        for ing in product.ingredients
                    ]
                else:
                    product_data["ingredients"] = []
                
                # Add date tracking information
                if product.date_product_users:
                    product_data["date_tracking"] = []
                    for date_info in product.date_product_users:
                        date_data = {
                            "id": date_info.id,
                            "product_id": date_info.product_id,
                            "quantity": date_info.quantity
                        }
                        
                        # Convert datetime objects to ISO strings
                        if date_info.date_manufactured:
                            date_data["date_manufactured"] = date_info.date_manufactured.isoformat()
                        if date_info.date_best_before:
                            date_data["date_best_before"] = date_info.date_best_before.isoformat()
                        if date_info.date_expired:
                            date_data["date_expired"] = date_info.date_expired.isoformat()
                        
                        product_data["date_tracking"].append(date_data)
                else:
                    product_data["date_tracking"] = []
                
                logger.info(f"Found product for code: {code}")
                return {
                    "found": True,
                    "code": code,
                    "product": product_data
                }
                
        except FreshAlertAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "found": False,
                "error": "Authentication failed. Please check your Bearer token.",
                "error_type": "authentication_error",
                "code": code,
                "product": None
            }
        except FreshAlertError as e:
            logger.error(f"Fresh Alert API error: {e}")
            return {
                "found": False,
                "error": f"Fresh Alert API error: {str(e)}",
                "error_type": "api_error",
                "error_code": getattr(e, 'error_code', None),
                "code": code,
                "product": None
            }
        except Exception as e:
            logger.error(f"Unexpected error in search_product_code: {e}")
            return {
                "found": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "code": code,
                "product": None
            }

    async def create_product_code(self, 
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
                                ingredients: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
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
            ingredients: List of ingredient dictionaries with fields: name, description, origin_country, is_allergen, etc.
            
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
            from utils.freshalert.models import CreateProductCodeRequest, IngredientDto
            
            config = FreshAlertConfig(bearer_token=self.bearer_token)
            
            # Convert ingredients dict to IngredientDto objects if provided
            ingredient_models = None
            if ingredients:
                ingredient_models = [
                    IngredientDto(**ing) if isinstance(ing, dict) else ing
                    for ing in ingredients
                ]
            
            # Create the request model
            product_request = CreateProductCodeRequest(
                code_number=code_number,
                code_type=code_type,
                product_name=product_name,
                brand=brand,
                manufacturer=manufacturer,
                description=description,
                category=category,
                country_of_origin=country_of_origin,
                usage_instruction=usage_instruction,
                storage_instruction=storage_instruction,
                image_url=image_url,
                nutrition_fact=nutrition_fact,
                label_key=label_key,
                phrase=phrase,
                ingredients=ingredient_models
            )
            
            async with FreshAlertClient(config) as client:
                created_product = await client.products.create_product_code(product_request)
                
                # Convert product to dictionary
                product_data = {
                    "id": created_product.id,
                    "code_number": created_product.code_number,
                    "code_type": created_product.code_type,
                    "product_name": created_product.product_name,
                    "brand": created_product.brand,
                    "manufacturer": created_product.manufacturer,
                    "description": created_product.description,
                    "image_url": created_product.image_url,
                    "usage_instruction": created_product.usage_instruction,
                    "storage_instruction": created_product.storage_instruction,
                    "country_of_origin": created_product.country_of_origin,
                    "category": created_product.category,
                    "nutrition_fact": created_product.nutrition_fact,
                    "label_key": created_product.label_key,
                    "phrase": created_product.phrase,
                    "date_tracking": []  # New product won't have date tracking yet
                }
                
                # Add ingredients if available
                if created_product.ingredients:
                    product_data["ingredients"] = [
                        {
                            "id": ing.id,
                            "off_id": ing.off_id,
                            "name": ing.name,
                            "description": ing.description,
                            "origin_country": ing.origin_country,
                            "is_allergen": ing.is_allergen,
                            "date_created": ing.date_created.isoformat() if ing.date_created else None
                        }
                        for ing in created_product.ingredients
                    ]
                else:
                    product_data["ingredients"] = []
                
                logger.info(f"Created product: {created_product.product_name} (ID: {created_product.id})")
                return {
                    "success": True,
                    "message": f"Successfully created product: {created_product.product_name}",
                    "product": product_data
                }
                
        except FreshAlertAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "success": False,
                "error": "Authentication failed. Please check your Bearer token.",
                "error_type": "authentication_error",
                "product": None
            }
        except FreshAlertError as e:
            logger.error(f"Fresh Alert API error: {e}")
            return {
                "success": False,
                "error": f"Fresh Alert API error: {str(e)}",
                "error_type": "api_error",
                "error_code": getattr(e, 'error_code', None),
                "product": None
            }
        except Exception as e:
            logger.error(f"Unexpected error in create_product_code: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "product": None
            }

    async def create_product_date(self,
                                product_id: str,
                                date_manufactured: Optional[str] = None,
                                date_best_before: Optional[str] = None,
                                date_expired: Optional[str] = None,
                                quantity: Optional[float] = None) -> Dict[str, Any]:
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
            from datetime import datetime
            from utils.freshalert.models import CreateProductDateRequest
            
            config = FreshAlertConfig(bearer_token=self.bearer_token)
            
            # Parse date strings to datetime objects
            parsed_dates = {}
            if date_manufactured:
                parsed_dates['date_manufactured'] = datetime.fromisoformat(date_manufactured.replace('Z', '+00:00'))
            if date_best_before:
                parsed_dates['date_best_before'] = datetime.fromisoformat(date_best_before.replace('Z', '+00:00'))
            if date_expired:
                parsed_dates['date_expired'] = datetime.fromisoformat(date_expired.replace('Z', '+00:00'))
            
            # Create the request model
            date_request = CreateProductDateRequest(
                product_id=product_id,
                quantity=quantity,
                **parsed_dates
            )
            
            async with FreshAlertClient(config) as client:
                created_date = await client.products.create_product_date(date_request)
                
                if not created_date:
                    return {
                        "success": False,
                        "error": "Failed to create product date entry",
                        "product_id": product_id,
                        "date_entry": None
                    }
                
                # Convert date entry to dictionary
                date_data = {
                    "id": created_date.id,
                    "product_id": created_date.product_id,
                    "quantity": created_date.quantity
                }
                
                # Convert datetime objects to ISO strings
                if created_date.date_manufactured:
                    date_data["date_manufactured"] = created_date.date_manufactured.isoformat()
                if created_date.date_best_before:
                    date_data["date_best_before"] = created_date.date_best_before.isoformat()
                if created_date.date_expired:
                    date_data["date_expired"] = created_date.date_expired.isoformat()
                
                logger.info(f"Created date entry for product: {product_id}")
                return {
                    "success": True,
                    "message": f"Successfully created date tracking for product: {product_id}",
                    "product_id": product_id,
                    "date_entry": date_data
                }
                
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            return {
                "success": False,
                "error": f"Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS): {str(e)}",
                "error_type": "validation_error",
                "product_id": product_id,
                "date_entry": None
            }
        except FreshAlertAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "success": False,
                "error": "Authentication failed. Please check your Bearer token.",
                "error_type": "authentication_error",
                "product_id": product_id,
                "date_entry": None
            }
        except FreshAlertError as e:
            logger.error(f"Fresh Alert API error: {e}")
            return {
                "success": False,
                "error": f"Fresh Alert API error: {str(e)}",
                "error_type": "api_error",
                "error_code": getattr(e, 'error_code', None),
                "product_id": product_id,
                "date_entry": None
            }
        except Exception as e:
            logger.error(f"Unexpected error in create_product_date: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "product_id": product_id,
                "date_entry": None
            }

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
            await search_product_by_name("apple")
        """
        try:
            config = FreshAlertConfig(bearer_token=self.bearer_token)
            
            async with FreshAlertClient(config) as client:
                products = await client.products.search_product_by_name(query)
                
                # Convert products to dictionary list
                response_data = {
                    "total_products": len(products),
                    "query": query,
                    "products": []
                }
                
                for product in products:
                    product_data = {
                        "brands": product.brands or "",
                        "code": product.code or "",
                        "product_name": product.product_name or "",
                        "image_url": product.image_url or ""        
                    }
                    
                    response_data["products"].append(product_data)
                
                logger.info(f"Found {len(products)} products matching query: {query}")
                return response_data
                
        except FreshAlertAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "error": "Authentication failed. Please check your Bearer token.",
                "error_type": "authentication_error",
                "query": query,
                "products": []
            }
        except FreshAlertError as e:
            logger.error(f"Fresh Alert API error: {e}")
            return {
                "error": f"Fresh Alert API error: {str(e)}",
                "error_type": "api_error",
                "error_code": getattr(e, 'error_code', None),
                "query": query,
                "products": []
            }
        except Exception as e:
            logger.error(f"Unexpected error in search_product_by_name: {e}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "query": query,
                "products": []
            }

    async def update_product_date(self,
                                 date_id: str,
                                 product_id: str,
                                 date_manufactured: Optional[str] = None,
                                 date_best_before: Optional[str] = None,
                                 date_expired: Optional[str] = None,
                                 quantity: Optional[float] = None) -> Dict[str, Any]:
        """
        Update an existing product date entry.
        
        This tool updates date tracking information for an existing product date entry.
        Use this to modify manufacturing dates, best before dates, expiration dates, or quantities.
        
        Args:
            date_id: ID of the date entry to update (required)
            date_manufactured: Manufacturing date in ISO format (e.g., "2024-01-15T10:30:00")
            date_best_before: Best before date in ISO format
            date_expired: Expiration date in ISO format
            quantity: Quantity of the product (e.g., 2.5 for 2.5 kg)
            
        Returns:
            Dictionary containing updated date entry information
            
        Examples:
            # Update expiration date of an entry
            await update_product_date(
                productId="a60e2e75-5ae3-4679-90de-7c7d29b24d56"
                date_id="12345678-1234-1234-1234-123456789012",
                date_expired="2024-12-31T23:59:59",
                quantity=0.5
            )
        """
        try:
            from datetime import datetime
            from utils.freshalert.models import UpdateProductDateRequest
            
            config = FreshAlertConfig(bearer_token=self.bearer_token)
            
            # Parse date strings to datetime objects
            parsed_dates = {}
            if date_manufactured:
                parsed_dates['date_manufactured'] = datetime.fromisoformat(date_manufactured.replace('Z', '+00:00'))
            if date_best_before:
                parsed_dates['date_best_before'] = datetime.fromisoformat(date_best_before.replace('Z', '+00:00'))
            if date_expired:
                parsed_dates['date_expired'] = datetime.fromisoformat(date_expired.replace('Z', '+00:00'))
            
            # Create the request model
            update_request = UpdateProductDateRequest(
                product_id=product_id,
                quantity=quantity,
                **parsed_dates
            )
            
            async with FreshAlertClient(config) as client:
                updated_date = await client.products.update_product_date(date_id, update_request)
                
                if not updated_date:
                    return {
                        "success": False,
                        "error": "Failed to update product date entry",
                        "date_id": date_id,
                        "date_entry": None
                    }
                
                # Convert date entry to dictionary
                date_data = {
                    "id": updated_date.id,
                    "product_id": updated_date.product_id,
                    "quantity": updated_date.quantity
                }
                
                # Convert datetime objects to ISO strings
                if updated_date.date_manufactured:
                    date_data["date_manufactured"] = updated_date.date_manufactured.isoformat()
                if updated_date.date_best_before:
                    date_data["date_best_before"] = updated_date.date_best_before.isoformat()
                if updated_date.date_expired:
                    date_data["date_expired"] = updated_date.date_expired.isoformat()
                
                logger.info(f"Updated date entry: {date_id}")
                return {
                    "success": True,
                    "message": f"Successfully updated date tracking entry: {date_id}",
                    "date_id": date_id,
                    "date_entry": date_data
                }
                
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            return {
                "success": False,
                "error": f"Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS): {str(e)}",
                "error_type": "validation_error",
                "date_id": date_id,
                "date_entry": None
            }
        except FreshAlertAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "success": False,
                "error": "Authentication failed. Please check your Bearer token.",
                "error_type": "authentication_error",
                "date_id": date_id,
                "date_entry": None
            }
        except FreshAlertError as e:
            logger.error(f"Fresh Alert API error: {e}")
            return {
                "success": False,
                "error": f"Fresh Alert API error: {str(e)}",
                "error_type": "api_error",
                "error_code": getattr(e, 'error_code', None),
                "date_id": date_id,
                "date_entry": None
            }
        except Exception as e:
            logger.error(f"Unexpected error in update_product_date: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "date_id": date_id,
                "date_entry": None
            }

    async def delete_product(self, product_id: str) -> Dict[str, Any]:
        """
        Soft delete a product from the user's list.
        
        This tool soft deletes a product, removing it from the user's active product list
        while preserving the data for potential recovery or audit purposes.
        
        Args:
            product_id: ID of the product to delete (required)
            
        Returns:
            Dictionary containing deletion confirmation
            
        Examples:
            # Delete a product
            await delete_product(product_id="12345678-1234-1234-1234-123456789012")
        """
        try:
            config = FreshAlertConfig(bearer_token=self.bearer_token)
            
            async with FreshAlertClient(config) as client:
                result = await client.products.delete_product(product_id)
                
                logger.info(f"Deleted product: {product_id}")
                return {
                    "success": True,
                    "message": f"Successfully deleted product: {product_id}",
                    "product_id": product_id,
                    "data": result
                }
                
        except FreshAlertAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "success": False,
                "error": "Authentication failed. Please check your Bearer token.",
                "error_type": "authentication_error",
                "product_id": product_id
            }
        except FreshAlertError as e:
            logger.error(f"Fresh Alert API error: {e}")
            return {
                "success": False,
                "error": f"Fresh Alert API error: {str(e)}",
                "error_type": "api_error",
                "error_code": getattr(e, 'error_code', None),
                "product_id": product_id
            }
        except Exception as e:
            logger.error(f"Unexpected error in delete_product: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "product_id": product_id
            }

