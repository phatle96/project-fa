from mcp.server.fastmcp import FastMCP, exceptions
from fastapi import HTTPException
from fresh_alert_tools import FreshAlertTools

from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware

import sys, os


def validateAuthToken():
    auth = mcp.get_context().request_context.request.headers.get("authorization", "")

    if not auth:
        raise HTTPException(
            status_code=401, detail="MCP error: Missing Authorization header"
        )
    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="MCP error: Invalid Authorization scheme"
        )
        
    token = auth.split(" ", 1)[1].strip()

    return token


PORT = 8015

if len(sys.argv) > 1:
    PORT = sys.argv[1]
    
ENV_PORT = os.getenv("FRESH_ALERT_MCP_PORT", "")

if ENV_PORT:
    PORT = ENV_PORT
    


mcp = FastMCP("FreshAlertMCP", port=PORT)






@mcp.tool()
async def get_user_products():
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

    token = validateAuthToken()
    tools = FreshAlertTools(bearer_token=token)

    return await tools.get_user_products()


@mcp.tool()
async def get_expired_products(days: int):
    """
    Get products that are about to expire for the current user.

    This tool retrieves products that will expire within
    a specified number of days. Useful for food waste prevention and
    meal planning based on expiring ingredients.

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

    token = validateAuthToken()
    tools = FreshAlertTools(bearer_token=token)

    return await tools.get_expired_products(days=days)


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

    token = validateAuthToken()
    tools = FreshAlertTools(bearer_token=token)

    return await tools.search_product_code(code=code)


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

    token = validateAuthToken()
    tools = FreshAlertTools(bearer_token=token)

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

    token = validateAuthToken()
    tools = FreshAlertTools(bearer_token=token)

    return await tools.create_product_date(
        product_id=product_id,
        date_manufactured=date_manufactured,
        date_best_before=date_best_before,
        date_expired=date_expired,
        quantity=quantity
    )


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

    token = validateAuthToken()
    tools = FreshAlertTools(bearer_token=token)

    return await tools.search_product_by_name(query=query)


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

    token = validateAuthToken()
    tools = FreshAlertTools(bearer_token=token)

    return await tools.update_product_date(
        date_id=date_id,
        product_id=product_id,
        date_manufactured=date_manufactured,
        date_best_before=date_best_before,
        date_expired=date_expired,
        quantity=quantity
    )


@mcp.tool()
async def delete_product(product_id: str):
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

    token = validateAuthToken()
    tools = FreshAlertTools(bearer_token=token)

    return await tools.delete_product(product_id=product_id)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
