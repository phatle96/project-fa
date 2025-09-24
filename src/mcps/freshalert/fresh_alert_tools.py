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

