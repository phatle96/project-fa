"""
MCP tools for Fresh Alert API integration.

This module provides tools for the agent to access user products and track
food expiration dates using the Fresh Alert API.
"""

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
            # Only try environment variable as fallback for development
            self.bearer_token = os.getenv("FRESH_ALERT_BEARER_TOKEN")
        
        if not self.bearer_token:
            raise ValueError(
                "Fresh Alert Bearer token is required. "
                "Pass bearer_token parameter or set FRESH_ALERT_BEARER_TOKEN environment variable."
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


# Standalone tool functions for MCP server
# These functions can be called by LangGraph agents

async def fresh_alert_get_user_products(bearer_token: str) -> Dict[str, Any]:
    """
    Get all products for the current user.
    
    This is a standalone tool function that can be used by LangGraph agents
    to retrieve all products associated with the authenticated user.
    
    Args:
        bearer_token: Fresh Alert Bearer token for authentication
        
    Returns:
        Dictionary containing user's products and metadata
        
    Example:
        result = await fresh_alert_get_user_products(bearer_token="your-token")
        print(f"Found {result['total_products']} products")
    """
    tools = FreshAlertTools(bearer_token=bearer_token)
    return await tools.get_user_products()


async def fresh_alert_get_expired_products(
    bearer_token: str,
    days: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get products that are expired or about to expire.
    
    This is a standalone tool function that can be used by LangGraph agents
    to retrieve products that have expired or will expire within a specified
    number of days.
    
    Args:
        bearer_token: Fresh Alert Bearer token for authentication
        days: Number of days to look ahead for expiring products (optional)
             If None, returns already expired products
             If positive integer, returns products expiring within that many days
        
    Returns:
        Dictionary containing expired/expiring products and metadata
        
    Examples:
        # Get already expired products
        result = await fresh_alert_get_expired_products(bearer_token="your-token")
        
        # Get products expiring in next 7 days
        result = await fresh_alert_get_expired_products(bearer_token="your-token", days=7)
    """
    tools = FreshAlertTools(bearer_token=bearer_token)
    return await tools.get_expired_products(days=days)


# Example usage and testing
if __name__ == "__main__":
    async def test_tools():
        """Test the Fresh Alert MCP tools"""
        bearer_token = os.getenv("FRESH_ALERT_BEARER_TOKEN")
        
        if not bearer_token:
            print("❌ Set FRESH_ALERT_BEARER_TOKEN environment variable to test the tools")
            return
        
        print("🧪 Testing Fresh Alert MCP Tools\n")
        
        # Test get user products
        print("📦 Testing get_user_products...")
        try:
            user_products = await fresh_alert_get_user_products(bearer_token)
            
            if 'error' in user_products:
                print(f"❌ Error: {user_products['error']}")
            else:
                print(f"✅ Found {user_products['total_products']} products")
                
                # Show first few products
                for i, product in enumerate(user_products['products'][:3], 1):
                    print(f"   {i}. {product['product_name']} ({product['brand']})")
                    if product['date_tracking']:
                        for date_info in product['date_tracking']:
                            if date_info.get('date_expired'):
                                print(f"      Expires: {date_info['date_expired']}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        print()
        
        # Test get expired products (already expired)
        print("⏰ Testing get_expired_products (already expired)...")
        try:
            expired_products = await fresh_alert_get_expired_products(bearer_token)
            
            if 'error' in expired_products:
                print(f"❌ Error: {expired_products['error']}")
            else:
                print(f"✅ Found {expired_products['total_products']} expired products")
                
                for i, product in enumerate(expired_products['products'][:3], 1):
                    print(f"   {i}. {product['product_name']} ({product['brand']})")
                    if product['date_tracking']:
                        for date_info in product['date_tracking']:
                            if date_info.get('days_until_expiry') is not None:
                                days = date_info['days_until_expiry']
                                status = "EXPIRED" if days < 0 else "expires today" if days == 0 else f"expires in {days} days"
                                print(f"      Status: {status}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        print()
        
        # Test get expiring products (next 7 days)
        print("📅 Testing get_expired_products (expiring in 7 days)...")
        try:
            expiring_products = await fresh_alert_get_expired_products(bearer_token, days=7)
            
            if 'error' in expiring_products:
                print(f"❌ Error: {expiring_products['error']}")
            else:
                print(f"✅ Found {expiring_products['total_products']} products expiring within 7 days")
                
                for i, product in enumerate(expiring_products['products'][:3], 1):
                    print(f"   {i}. {product['product_name']} ({product['brand']})")
                    if product['date_tracking']:
                        for date_info in product['date_tracking']:
                            if date_info.get('days_until_expiry') is not None:
                                days = date_info['days_until_expiry']
                                if days >= 0:
                                    status = "expires today" if days == 0 else f"expires in {days} days"
                                    print(f"      Status: {status}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    # Run tests
    asyncio.run(test_tools())