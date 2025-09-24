"""
Example usage of the Fresh Alert API client.

This example demonstrates how to use the Fresh Alert client to:
1. Get all user products
2. Get expired/expiring products
3. Handle authentication
4. Handle errors properly
"""

import asyncio
import logging
from typing import List

# Import the Fresh Alert client
from src.utils.freshalert import (
    FreshAlertClient,
    FreshAlertConfig,
    ProductResponseDto,
    FreshAlertError
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demonstrate_client_usage():
    """Demonstrate basic Fresh Alert client usage"""
    
    # IMPORTANT: In production LangGraph usage, the Bearer token should be passed 
    # as an argument from request headers, not from environment variables
    
    # Method 1: Direct token passing (recommended for LangGraph)
    bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJnWm9HRG5YbGJCcndDMTQ2SnNBOEswRG5yTWxZNWZzODJjOUhXb3lVYVhNIn0.eyJleHAiOjE3NTgzMDg2ODMsImlhdCI6MTc1ODI3MjY4NCwiYXV0aF90aW1lIjoxNzU4MjcyNjgzLCJqdGkiOiJvbnJ0YWM6MmY1ZjY4NzAtYjAzOC02NTMwLWNkNmQtMzA4YmI1ZmQ1ZmFlIiwiaXNzIjoiaHR0cHM6Ly9rYy5pbHdpdGguaW8vcmVhbG1zL2lkZW50aXR5IiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjRjZjU3OThmLTA4NDQtNGI4Ni04OWM3LTNhZDIxZjVjNDk1NCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZyb250ZW5kIiwic2lkIjoiYzQ2Y2RjMDItYzA4OC00ZmU3LWEwOTItOTE5ZmYzMGU5NGFiIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwOi8vbG9jYWxob3N0OjUxMjkvKiIsImh0dHA6Ly81MS43OS4yMTkuNzE6MzAwMCIsImh0dHA6Ly9sb2NhbGhvc3Q6NDIwMCIsImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1pZGVudGl0eSIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiVHkgTGUiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ0eWxlIiwiZ2l2ZW5fbmFtZSI6IlR5IiwiZmFtaWx5X25hbWUiOiJMZSIsImVtYWlsIjoidHlsZUBlbWFpbC5jb20ifQ.I-UgkYsE2BJpOEVuBWik0Cl2IEgbEh03S8BdpEqsv48ESXbzWy_XthZjN-kxrnGTX3-CqXr1O_ll4BGfFE1KcWVFn5-1_CV-bLrFqhNw63tTuzuV-M4SdQx_GRrxuZjYim8t9XUJyuPKglBaB2GSBzlluLBVOXHHnsWzWgUpNZ9O1RN-UOcnIji5aRTW9tyreWAUjjil1OvsG81Ekoo8vBvIHvQtSDngwZF87Sw5sPoV-OXSeyq7rhGi2h5nUFRBXZw07vzrhOx4x3dYIEdrCXs2IghQLs9Stp6SmrfjXRwG4DecdP1QUe8tK-KwL2oGgmRaD0eVpEZo0lJOKaam-A"  # This would come from request headers
    config = FreshAlertConfig(bearer_token=bearer_token)
    
    # Method 2: Environment variables (only for development/testing)
    # config = FreshAlertConfig()  # Loads from FRESH_ALERT_BEARER_TOKEN if set
    
    # Create client with configuration
    client = FreshAlertClient(config)
    
    try:
        # Use async context manager for proper resource management
        async with client:
            # Check if client is properly authenticated
            if not client.is_authenticated():
                logger.warning("Client is not authenticated! Pass Bearer token as argument.")
                logger.info("For LangGraph: Extract token from request headers")
                return
            
            # Perform health check
            logger.info("Performing health check...")
            await client.health_check()
            logger.info("✓ Health check passed")
            
            # Get all user products
            logger.info("Fetching all user products...")
            all_products = await client.get_my_products()
            logger.info(f"✓ Found {len(all_products)} total products")
            
            # Print product details
            if all_products:
                for i, product in enumerate(all_products[:3], 1):  # Show first 3
                    logger.info(f"  {i}. {product.product_name} ({product.brand})")
                    if product.date_product_users:
                        for date_info in product.date_product_users:
                            if date_info.date_expired:
                                logger.info(f"     Expires: {date_info.date_expired}")
            
            # Get products expiring in the next 7 days
            logger.info("\nFetching products expiring in next 7 days...")
            expiring_products = await client.get_expiring_products(days=7)
            logger.info(f"✓ Found {len(expiring_products)} products expiring soon")
            
            # Get products expiring in the next 3 days
            logger.info("\nFetching products expiring in next 3 days...")
            urgent_expiring = await client.get_expiring_products(days=3)
            logger.info(f"✓ Found {len(urgent_expiring)} products expiring urgently")
            
            # Get already expired products
            logger.info("\nFetching already expired products...")
            expired_products = await client.get_expired_products()
            logger.info(f"✓ Found {len(expired_products)} expired products")
            
            # Using the lower-level API directly
            logger.info("\nUsing lower-level Products API...")
            products_via_api = await client.products.get_user_products()
            logger.info(f"✓ Found {len(products_via_api)} products via direct API call")
            
    except FreshAlertError as e:
        logger.error(f"Fresh Alert API error: {e}")
        if hasattr(e, 'status_code'):
            logger.error(f"Status code: {e.status_code}")
        if hasattr(e, 'error_code'):
            logger.error(f"Error code: {e.error_code}")
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


async def demonstrate_authentication_methods():
    """Demonstrate different authentication methods"""
    
    logger.info("=== Authentication Methods Demo ===")
    
    # Method 1: Direct token passing (recommended for LangGraph)
    token_from_headers = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJnWm9HRG5YbGJCcndDMTQ2SnNBOEswRG5yTWxZNWZzODJjOUhXb3lVYVhNIn0.eyJleHAiOjE3NTgzMDg2ODMsImlhdCI6MTc1ODI3MjY4NCwiYXV0aF90aW1lIjoxNzU4MjcyNjgzLCJqdGkiOiJvbnJ0YWM6MmY1ZjY4NzAtYjAzOC02NTMwLWNkNmQtMzA4YmI1ZmQ1ZmFlIiwiaXNzIjoiaHR0cHM6Ly9rYy5pbHdpdGguaW8vcmVhbG1zL2lkZW50aXR5IiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjRjZjU3OThmLTA4NDQtNGI4Ni04OWM3LTNhZDIxZjVjNDk1NCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZyb250ZW5kIiwic2lkIjoiYzQ2Y2RjMDItYzA4OC00ZmU3LWEwOTItOTE5ZmYzMGU5NGFiIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwOi8vbG9jYWxob3N0OjUxMjkvKiIsImh0dHA6Ly81MS43OS4yMTkuNzE6MzAwMCIsImh0dHA6Ly9sb2NhbGhvc3Q6NDIwMCIsImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1pZGVudGl0eSIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiVHkgTGUiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ0eWxlIiwiZ2l2ZW5fbmFtZSI6IlR5IiwiZmFtaWx5X25hbWUiOiJMZSIsImVtYWlsIjoidHlsZUBlbWFpbC5jb20ifQ.I-UgkYsE2BJpOEVuBWik0Cl2IEgbEh03S8BdpEqsv48ESXbzWy_XthZjN-kxrnGTX3-CqXr1O_ll4BGfFE1KcWVFn5-1_CV-bLrFqhNw63tTuzuV-M4SdQx_GRrxuZjYim8t9XUJyuPKglBaB2GSBzlluLBVOXHHnsWzWgUpNZ9O1RN-UOcnIji5aRTW9tyreWAUjjil1OvsG81Ekoo8vBvIHvQtSDngwZF87Sw5sPoV-OXSeyq7rhGi2h5nUFRBXZw07vzrhOx4x3dYIEdrCXs2IghQLs9Stp6SmrfjXRwG4DecdP1QUe8tK-KwL2oGgmRaD0eVpEZo0lJOKaam-A"  # Would come from request
    config1 = FreshAlertConfig(bearer_token=token_from_headers)
    logger.info(f"Method 1 - Direct token: Authenticated = {bool(config1.bearer_token)}")
    
    # Method 2: Environment variables (only for development/testing)
    config2 = FreshAlertConfig()  # Loads from FRESH_ALERT_BEARER_TOKEN if set
    logger.info(f"Method 2 - Env vars: Authenticated = {bool(config2.bearer_token)}")
    
    # Method 3: API Key (alternative, if supported by Fresh Alert API)
    config3 = FreshAlertConfig(api_key="your-api-key-here")
    logger.info(f"Method 3 - API Key: Authenticated = {bool(config3.api_key)}")
    
    logger.info("\nNote: For LangGraph integration, use Method 1 with tokens from request headers")


def demonstrate_configuration():
    """Demonstrate configuration options"""
    
    logger.info("=== Configuration Options Demo ===")
    
    # Custom configuration with dynamic token (typical LangGraph usage)
    bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJnWm9HRG5YbGJCcndDMTQ2SnNBOEswRG5yTWxZNWZzODJjOUhXb3lVYVhNIn0.eyJleHAiOjE3NTgzMDg2ODMsImlhdCI6MTc1ODI3MjY4NCwiYXV0aF90aW1lIjoxNzU4MjcyNjgzLCJqdGkiOiJvbnJ0YWM6MmY1ZjY4NzAtYjAzOC02NTMwLWNkNmQtMzA4YmI1ZmQ1ZmFlIiwiaXNzIjoiaHR0cHM6Ly9rYy5pbHdpdGguaW8vcmVhbG1zL2lkZW50aXR5IiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjRjZjU3OThmLTA4NDQtNGI4Ni04OWM3LTNhZDIxZjVjNDk1NCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZyb250ZW5kIiwic2lkIjoiYzQ2Y2RjMDItYzA4OC00ZmU3LWEwOTItOTE5ZmYzMGU5NGFiIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwOi8vbG9jYWxob3N0OjUxMjkvKiIsImh0dHA6Ly81MS43OS4yMTkuNzE6MzAwMCIsImh0dHA6Ly9sb2NhbGhvc3Q6NDIwMCIsImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1pZGVudGl0eSIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiVHkgTGUiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ0eWxlIiwiZ2l2ZW5fbmFtZSI6IlR5IiwiZmFtaWx5X25hbWUiOiJMZSIsImVtYWlsIjoidHlsZUBlbWFpbC5jb20ifQ.I-UgkYsE2BJpOEVuBWik0Cl2IEgbEh03S8BdpEqsv48ESXbzWy_XthZjN-kxrnGTX3-CqXr1O_ll4BGfFE1KcWVFn5-1_CV-bLrFqhNw63tTuzuV-M4SdQx_GRrxuZjYim8t9XUJyuPKglBaB2GSBzlluLBVOXHHnsWzWgUpNZ9O1RN-UOcnIji5aRTW9tyreWAUjjil1OvsG81Ekoo8vBvIHvQtSDngwZF87Sw5sPoV-OXSeyq7rhGi2h5nUFRBXZw07vzrhOx4x3dYIEdrCXs2IghQLs9Stp6SmrfjXRwG4DecdP1QUe8tK-KwL2oGgmRaD0eVpEZo0lJOKaam-A"  # From request headers
    config = FreshAlertConfig(
        bearer_token=bearer_token,     # Pass token dynamically
        timeout=45.0,          # 45 second timeout
        max_retries=5,         # Retry up to 5 times
        retry_delay=2.0,       # 2 second delay between retries
        rate_limit=5.0         # Max 5 requests per second
    )
    
    logger.info(f"Base URL: {config.full_base_url}")
    logger.info(f"Timeout: {config.timeout}s")
    logger.info(f"Max retries: {config.max_retries}")
    logger.info(f"Rate limit: {config.rate_limit} req/s")
    logger.info(f"Auth headers: {config.auth_headers}")


async def demonstrate_langgraph_integration():
    """Demonstrate how to use with LangGraph request headers"""
    
    logger.info("=== LangGraph Integration Demo ===")
    
    # Simulate a LangGraph config with headers (this would come from actual request)
    mock_langgraph_config = {
        "configurable": {
            "headers": {
                "Authentication": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "Content-Type": "application/json"
            }
        }
    }
    
    def get_auth_token(config: dict) -> str | None:
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
    
    # Extract token from mock request
    token = get_auth_token(mock_langgraph_config)
    logger.info(f"Extracted token from headers: {token[:20]}..." if token else "No token found")
    
    if token:
        # Create Fresh Alert client with extracted token
        config = FreshAlertConfig(bearer_token=token)
        
        async with FreshAlertClient(config) as client:
            logger.info("✓ Fresh Alert client created with dynamic token")
            logger.info("✓ Ready for LangGraph agent integration")
            
            # This is where you would call actual API methods
            # products = await client.get_my_products()
    else:
        logger.warning("✗ No authentication token found in headers")


if __name__ == "__main__":
    """Run the examples"""
    
    # Demonstrate configuration
    demonstrate_configuration()
    print()
    
    # Run async examples
    asyncio.run(demonstrate_authentication_methods())
    print()
    
    # Demonstrate LangGraph integration
    asyncio.run(demonstrate_langgraph_integration())
    print()
    
    # Main client usage demo
    asyncio.run(demonstrate_client_usage())