from mcp.server.fastmcp import FastMCP, exceptions
from fastapi import HTTPException
from fresh_alert_tools import FreshAlertTools

mcp = FastMCP("FreshAlertMCP", port=8015)


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
    print("---->>> token: ", token)
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


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
