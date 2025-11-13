"""
FreshAlert MCP Server V2

Improved MCP server implementation using generated Swagger client.
Enhancements over v1:
- Better input validation with detailed error messages
- Consistent error handling across all tools
- Enhanced logging for debugging
- Type-safe API calls using generated client
- Proper request context validation
"""

from mcp.server.fastmcp import FastMCP
from fastapi import HTTPException
from fresh_alert_tools_v2 import FreshAlertToolsV2
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_auth_token() -> str:
    """
    Validate and extract bearer token from request headers.
    
    Returns:
        str: Bearer token
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    auth = mcp.get_context().request_context.request.headers.get("authorization", "")

    if not auth:
        logger.error("Missing Authorization header")
        raise HTTPException(
            status_code=401, 
            detail="MCP error: Missing Authorization header"
        )
    
    if not auth.startswith("Bearer "):
        logger.error("Invalid Authorization scheme")
        raise HTTPException(
            status_code=401, 
            detail="MCP error: Invalid Authorization scheme. Must use 'Bearer <token>'"
        )
        
    token = auth.split(" ", 1)[1].strip()
    
    if not token:
        logger.error("Empty bearer token")
        raise HTTPException(
            status_code=401, 
            detail="MCP error: Bearer token is empty"
        )
    
    return token


# Configure port
PORT = 8015

if len(sys.argv) > 1:
    PORT = sys.argv[1]
    
ENV_PORT = os.getenv("FRESH_ALERT_MCP_PORT", "")

if ENV_PORT:
    PORT = ENV_PORT

logger.info(f"Initializing FreshAlert MCP Server V2 on port {PORT}")

mcp = FastMCP("FreshAlertMCP_V2", port=PORT)


@mcp.tool()
async def get_user_products(is_expired: int = None):
    """
    Get products for the current user with optional expiration filtering.

    This tool retrieves products associated with the authenticated user,
    including product details, expiration dates, and quantity information.
    Use the is_expired parameter to filter products by their expiration status.

    Args:
        is_expired: Optional filter for product expiration status (default: None)
                   - 1: Get only expired products
                   - -1: Get only non-expired products  
                   - 0 or None: Get all products (expired and non-expired)

    Returns:
        Dictionary containing user's products and metadata

    Examples:
        # Get all user products (expired and non-expired)
        await get_user_products()
        
        # Get only non-expired products (for personalized suggestions)
        await get_user_products(is_expired=-1)
        
        # Get only expired products
        await get_user_products(is_expired=1)
        
        # Get all products explicitly
        await get_user_products(is_expired=0)
    """
    try:
        # Input validation
        if is_expired is not None and is_expired not in [1, -1, 0]:
            raise HTTPException(
                status_code=400,
                detail="is_expired parameter must be 1 (expired), -1 (non-expired), or 0 (all products)"
            )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        return await tools.get_user_products(is_expired=is_expired)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_user_products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@mcp.tool()
async def get_expired_products(days: int):
    """
    Get products that are about to expire for the current user.

    This tool retrieves products that will expire within
    a specified number of days. Useful for food waste prevention and
    meal planning based on expiring ingredients.

    Args:
        days: Number of days to look ahead for expiring products (must be non-negative)

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
        if not isinstance(days, (int, float)):
            raise HTTPException(
                status_code=400,
                detail="days parameter must be a number"
            )
        
        if days < 0:
            raise HTTPException(
                status_code=400,
                detail="days parameter must be non-negative"
            )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        return await tools.get_expired_products(days=int(days))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_expired_products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@mcp.tool()
async def search_product_code(code: str):
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
        if not code or not isinstance(code, str):
            raise HTTPException(
                status_code=400,
                detail="code parameter is required and must be a string"
            )
        
        if not code.strip():
            raise HTTPException(
                status_code=400,
                detail="code parameter cannot be empty"
            )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        return await tools.search_product_code(code=code)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search_product_code: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@mcp.tool()
async def create_product_code(
    code_number: str,
    code_type: str = None,
    product_name: str = None,
    brand: str = None,
    manufacturer: str = None,
    description: str = None,
    category: str = None,
    country_of_origin: str = None,
    usage_instruction: str = None,
    storage_instruction: str = None,
    image_url: list = None,
    nutrition_fact: str = None,
    label_key: str = None,
    phrase: str = None,
    ingredients: list = None
):
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
        
        # Create a product with ingredients
        await create_product_code(
            code_number="9876543210987",
            product_name="Chocolate Bar",
            brand="Sweet Co",
            ingredients=[
                {"name": "Cocoa", "is_allergen": False},
                {"name": "Milk", "is_allergen": True}
            ]
        )
    """
    try:
        # Input validation
        if not code_number or not isinstance(code_number, str):
            raise HTTPException(
                status_code=400,
                detail="code_number parameter is required and must be a string"
            )
        
        if not code_number.strip():
            raise HTTPException(
                status_code=400,
                detail="code_number parameter cannot be empty"
            )
        
        if image_url is not None and not isinstance(image_url, list):
            raise HTTPException(
                status_code=400,
                detail="image_url parameter must be a list"
            )
        
        if ingredients is not None and not isinstance(ingredients, list):
            raise HTTPException(
                status_code=400,
                detail="ingredients parameter must be a list"
            )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        
        return await tools.create_product_code(
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
            ingredients=ingredients
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_product_code: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@mcp.tool()
async def create_product_date(
    product_id: str,
    date_manufactured: str = None,
    date_best_before: str = None,
    date_expired: str = None,
    quantity: float = None
):
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
        if not product_id or not isinstance(product_id, str):
            raise HTTPException(
                status_code=400,
                detail="product_id parameter is required and must be a string"
            )
        
        if not product_id.strip():
            raise HTTPException(
                status_code=400,
                detail="product_id parameter cannot be empty"
            )
        
        if quantity is not None and not isinstance(quantity, (int, float)):
            raise HTTPException(
                status_code=400,
                detail="quantity parameter must be a number"
            )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        
        return await tools.create_product_date(
            product_id=product_id,
            date_manufactured=date_manufactured,
            date_best_before=date_best_before,
            date_expired=date_expired,
            quantity=quantity
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_product_date: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@mcp.tool()
async def search_product_by_name(query: str):
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
        if not query or not isinstance(query, str):
            raise HTTPException(
                status_code=400,
                detail="query parameter is required and must be a string"
            )
        
        if not query.strip():
            raise HTTPException(
                status_code=400,
                detail="query parameter cannot be empty"
            )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        return await tools.search_product_by_name(query=query)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search_product_by_name: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@mcp.tool()
async def update_product_date(
    date_id: str,
    product_id: str,
    date_manufactured: str = None,
    date_best_before: str = None,
    date_expired: str = None,
    quantity: float = None
):
    """
    Update an existing product date entry.

    This tool updates date tracking information for an existing product date entry.
    Use this to modify manufacturing dates, best before dates, expiration dates, or quantities.

    Args:
        date_id: ID of the date entry to update (required)
        product_id: ID of the product that linked to the date_id (required)
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
        if not date_id or not isinstance(date_id, str):
            raise HTTPException(
                status_code=400,
                detail="date_id parameter is required and must be a string"
            )
        
        if not date_id.strip():
            raise HTTPException(
                status_code=400,
                detail="date_id parameter cannot be empty"
            )
        
        if not product_id or not isinstance(product_id, str):
            raise HTTPException(
                status_code=400,
                detail="product_id parameter is required and must be a string"
            )
        
        if not product_id.strip():
            raise HTTPException(
                status_code=400,
                detail="product_id parameter cannot be empty"
            )
        
        if quantity is not None and not isinstance(quantity, (int, float)):
            raise HTTPException(
                status_code=400,
                detail="quantity parameter must be a number"
            )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        
        return await tools.update_product_date(
            date_id=date_id,
            product_id=product_id,
            date_manufactured=date_manufactured,
            date_best_before=date_best_before,
            date_expired=date_expired,
            quantity=quantity
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_product_date: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@mcp.tool()
async def delete_product_date(date_ids: list):
    """
    Soft delete product date entries by their IDs.

    This tool soft deletes one or more product date entries (date tracking records),
    removing them from active tracking while preserving the data for audit purposes.
    Use this when you want to remove date tracking entries for products.

    Args:
        date_ids: List of date entry IDs to delete (required, must be non-empty list of strings)

    Returns:
        Dictionary containing deletion confirmation and count

    Examples:
        # Delete a single date entry
        await delete_product_date(date_ids=["12345678-1234-1234-1234-123456789012"])

        # Delete multiple date entries at once
        await delete_product_date(date_ids=[
            "12345678-1234-1234-1234-123456789012",
            "87654321-4321-4321-4321-210987654321"
        ])
    """
    try:
        # Input validation
        if not date_ids or not isinstance(date_ids, list):
            raise HTTPException(
                status_code=400,
                detail="date_ids parameter is required and must be a list"
            )
        
        if len(date_ids) == 0:
            raise HTTPException(
                status_code=400,
                detail="date_ids list cannot be empty"
            )
        
        # Validate each item in the list
        for i, date_id in enumerate(date_ids):
            if not date_id or not isinstance(date_id, str):
                raise HTTPException(
                    status_code=400,
                    detail=f"date_ids[{i}] must be a non-empty string"
                )
            if not date_id.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"date_ids[{i}] cannot be empty or whitespace"
                )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        return await tools.delete_product_date(date_ids=date_ids)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_product_date: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@mcp.tool()
async def delete_product(product_ids: list):
    """
    Soft delete products from the user's list.

    This tool soft deletes one or more products, removing them from the user's active 
    product list while preserving the data for potential recovery or audit purposes.
    Use this when you want to remove products from tracking.

    Args:
        product_ids: List of product IDs to delete (required, must be non-empty list of strings)

    Returns:
        Dictionary containing deletion confirmation and count

    Examples:
        # Delete a single product
        await delete_product(product_ids=["12345678-1234-1234-1234-123456789012"])

        # Delete multiple products at once
        await delete_product(product_ids=[
            "12345678-1234-1234-1234-123456789012",
            "87654321-4321-4321-4321-210987654321"
        ])
    """
    try:
        # Input validation
        if not product_ids or not isinstance(product_ids, list):
            raise HTTPException(
                status_code=400,
                detail="product_ids parameter is required and must be a list"
            )
        
        if len(product_ids) == 0:
            raise HTTPException(
                status_code=400,
                detail="product_ids list cannot be empty"
            )
        
        # Validate each item in the list
        for i, product_id in enumerate(product_ids):
            if not product_id or not isinstance(product_id, str):
                raise HTTPException(
                    status_code=400,
                    detail=f"product_ids[{i}] must be a non-empty string"
                )
            if not product_id.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"product_ids[{i}] cannot be empty or whitespace"
                )
        
        token = validate_auth_token()
        tools = FreshAlertToolsV2(bearer_token=token)
        return await tools.delete_product(product_ids=product_ids)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_product: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


if __name__ == "__main__":
    logger.info("Starting FreshAlert MCP Server V2")
    mcp.run(transport="streamable-http")
