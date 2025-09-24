# Fresh Alert MCP Tools

Model Context Protocol (MCP) tools for integrating Fresh Alert API functionality into LangGraph agents and other AI applications.

## Overview

The Fresh Alert MCP tools provide seamless integration with the Fresh Alert API, enabling AI agents to:

- **Track user products** and their expiration dates
- **Monitor food freshness** and prevent waste
- **Plan meals** based on expiring ingredients
- **Alert users** about products that need attention

## Features

- 🔐 **Secure authentication** with Bearer token support
- 📦 **Product management** - Get all user products with detailed information
- ⏰ **Expiration tracking** - Monitor expired and expiring products
- 🧠 **AI-friendly responses** - Structured data optimized for LLM processing
- 🔄 **Async support** - Non-blocking operations for better performance
- 🛡️ **Comprehensive error handling** - Graceful handling of API errors
- 🧪 **Fully tested** - Complete test suite with integration examples

## Installation

The tools depend on the Fresh Alert client wrapper:

```bash
# Ensure you have the Fresh Alert client installed
pip install httpx pydantic
```

## Quick Start

### Basic Usage

```python
import asyncio
from fresh_alert_mcp import fresh_alert_get_user_products, fresh_alert_get_expired_products

async def main():
    bearer_token = "your-fresh-alert-bearer-token"
    
    # Get all user products
    products = await fresh_alert_get_user_products(bearer_token)
    print(f"Found {products['total_products']} products")
    
    # Get products expiring in next 7 days
    expiring = await fresh_alert_get_expired_products(bearer_token, days=7)
    print(f"Found {expiring['total_products']} expiring products")

asyncio.run(main())
```

### LangGraph Integration

```python
from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from fresh_alert_mcp import fresh_alert_get_user_products, fresh_alert_get_expired_products

def get_auth_token(config: RunnableConfig) -> str | None:
    """Extract authentication token from request headers"""
    if not config:
        return None
    
    configurable = config.get("configurable", {})
    headers = configurable.get("headers", {})
    
    auth_header = headers.get("Authentication") or headers.get("authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    
    return None

async def food_tracking_agent(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """LangGraph agent that uses Fresh Alert tools"""
    
    # Extract token from request headers
    token = get_auth_token(config)
    if not token:
        raise ValueError("Authentication token is required")
    
    # Get user's products
    products = await fresh_alert_get_user_products(token)
    
    # Get products expiring soon
    expiring = await fresh_alert_get_expired_products(token, days=3)
    
    # Update agent state
    state["user_products"] = products
    state["expiring_products"] = expiring
    
    return state
```

## API Reference

### `fresh_alert_get_user_products(bearer_token: str)`

Get all products for the authenticated user.

**Parameters:**
- `bearer_token` (str): Fresh Alert Bearer token for authentication

**Returns:**
```python
{
    "total_products": 15,
    "products": [
        {
            "id": "uuid-string",
            "code_number": "1234567890123",
            "code_type": "UPC",
            "product_name": "Organic Milk",
            "brand": "Fresh Brand",
            "manufacturer": "Fresh Dairy Co",
            "description": "2% Organic Milk",
            "image_url": ["https://..."],
            "usage_instruction": "Shake well before use",
            "storage_instruction": "Refrigerate after opening",
            "country_of_origin": "USA",
            "category": "Dairy",
            "nutrition_fact": "...",
            "label_key": "organic",
            "phrase": "Best before date on cap",
            "date_tracking": [
                {
                    "id": "date-uuid",
                    "product_id": "product-uuid",
                    "quantity": 2.0,
                    "date_manufactured": "2024-09-01T00:00:00Z",
                    "date_best_before": "2024-09-25T00:00:00Z",
                    "date_expired": "2024-09-30T00:00:00Z"
                }
            ]
        }
    ]
}
```

**Error Response:**
```python
{
    "error": "Authentication failed. Please check your Bearer token.",
    "error_type": "authentication_error",
    "products": []
}
```

### `fresh_alert_get_expired_products(bearer_token: str, days: Optional[int] = None)`

Get products that are expired or about to expire.

**Parameters:**
- `bearer_token` (str): Fresh Alert Bearer token for authentication
- `days` (Optional[int]): Number of days to look ahead for expiring products
  - `None`: Returns already expired products
  - `7`: Returns products expiring within 7 days
  - `0`: Returns products expiring today

**Returns:**
```python
{
    "search_criteria": {
        "days": 7,
        "description": "products expiring within 7 days"
    },
    "total_products": 3,
    "products": [
        {
            "id": "uuid-string",
            "product_name": "Greek Yogurt",
            "brand": "Healthy Brand",
            # ... other product fields ...
            "date_tracking": [
                {
                    "id": "date-uuid",
                    "product_id": "product-uuid",
                    "quantity": 1.0,
                    "date_expired": "2024-09-25T00:00:00Z",
                    "days_until_expiry": 3,
                    "is_expired": false,
                    "expires_today": false
                }
            ]
        }
    ]
}
```

## Tool Class Usage

For advanced usage, you can use the `FreshAlertTools` class directly:

```python
from fresh_alert_mcp import FreshAlertTools

async def advanced_usage():
    tools = FreshAlertTools(bearer_token="your-token")
    
    # Get user products with error handling
    try:
        products = await tools.get_user_products()
        if 'error' in products:
            print(f"Error: {products['error']}")
        else:
            print(f"Success: {products['total_products']} products")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Get expired products with custom logic
    expired = await tools.get_expired_products()
    expiring_soon = await tools.get_expired_products(days=3)
    expiring_week = await tools.get_expired_products(days=7)
```

## Error Handling

The tools provide comprehensive error handling with specific error types:

### Error Types

- **`authentication_error`**: Invalid or missing Bearer token
- **`api_error`**: Fresh Alert API returned an error
- **`unexpected_error`**: Unexpected exception occurred

### Error Response Format

```python
{
    "error": "Human-readable error message",
    "error_type": "authentication_error",
    "error_code": "INVALID_TOKEN",  # Optional API error code
    "products": []  # Always present, empty on error
}
```

### Best Practices

```python
async def handle_fresh_alert_call(bearer_token: str):
    """Example of proper error handling"""
    
    try:
        result = await fresh_alert_get_user_products(bearer_token)
        
        if 'error' in result:
            error_type = result.get('error_type', 'unknown')
            
            if error_type == 'authentication_error':
                # Handle authentication issues
                return "Please check your Fresh Alert login credentials."
            elif error_type == 'api_error':
                # Handle API issues
                return "Fresh Alert service is temporarily unavailable."
            else:
                return f"Error accessing your products: {result['error']}"
        
        # Process successful response
        return f"Found {result['total_products']} products in your account."
        
    except Exception as e:
        # Handle unexpected errors
        return f"Unexpected error: {str(e)}"
```

## Testing

### Run Tests

```bash
# Set your Bearer token
export FRESH_ALERT_BEARER_TOKEN="your-token-here"

# Run the test suite
cd src/mcps/freshalert
python test_fresh_alert_mcp.py
```

### Test Output Example

```
🧪 Starting Fresh Alert MCP Tools Test Suite
============================================================
✅ Get User Products - Success Case: PASSED - Found 15 products
✅ Get Expired Products - No Days Parameter: PASSED - Found 2 expired products
✅ Get Expired Products - With Days Parameter: PASSED - Found 5 products expiring within 7 days
✅ Standalone Functions: PASSED - Both standalone functions work correctly
✅ Error Handling - Invalid Token: PASSED - Properly handles authentication errors
✅ Data Format Validation: PASSED - All dates are in correct ISO format
============================================================
🏁 Test Suite Summary
✅ Tests Passed: 6
❌ Tests Failed: 0

📊 Success Rate: 100.0%

🔗 Testing LangGraph Integration Scenario
--------------------------------------------------
1. Extracting token from mock LangGraph config...
   Token: eyJhbGciOi...
2. Calling Fresh Alert tools with extracted token...
   ✅ Successfully retrieved 15 products
3. Testing expiring products...
   ✅ Found 5 products expiring within 7 days
🎉 Integration test completed successfully!
```

## Example Use Cases

### 1. Meal Planning Assistant

```python
async def suggest_meals_from_expiring_products(bearer_token: str, days: int = 3):
    """Suggest meals based on products expiring soon"""
    
    expiring = await fresh_alert_get_expired_products(bearer_token, days=days)
    
    if 'error' in expiring:
        return "Unable to check expiring products."
    
    if expiring['total_products'] == 0:
        return "No products expiring soon. You're all set!"
    
    suggestions = []
    for product in expiring['products']:
        name = product['product_name']
        category = product.get('category', 'Unknown')
        
        # Get expiration info
        for date_info in product['date_tracking']:
            if 'days_until_expiry' in date_info:
                days_left = date_info['days_until_expiry']
                if days_left <= days:
                    suggestions.append(f"{name} ({category}) - expires in {days_left} days")
    
    if suggestions:
        return f"Use these ingredients soon:\n" + "\n".join(suggestions)
    else:
        return "No products need immediate attention."
```

### 2. Food Waste Prevention

```python
async def check_food_waste_risk(bearer_token: str):
    """Check for food waste risk and provide alerts"""
    
    # Get already expired products
    expired = await fresh_alert_get_expired_products(bearer_token)
    
    # Get products expiring today
    expiring_today = await fresh_alert_get_expired_products(bearer_token, days=0)
    
    alerts = []
    
    if not 'error' in expired and expired['total_products'] > 0:
        alerts.append(f"⚠️ {expired['total_products']} products have already expired!")
    
    if not 'error' in expiring_today and expiring_today['total_products'] > 0:
        alerts.append(f"🚨 {expiring_today['total_products']} products expire today!")
    
    return alerts if alerts else ["✅ No immediate food waste concerns."]
```

### 3. Inventory Management

```python
async def get_inventory_summary(bearer_token: str):
    """Get comprehensive inventory summary"""
    
    all_products = await fresh_alert_get_user_products(bearer_token)
    expired = await fresh_alert_get_expired_products(bearer_token)
    expiring_week = await fresh_alert_get_expired_products(bearer_token, days=7)
    
    if any('error' in result for result in [all_products, expired, expiring_week]):
        return "Unable to retrieve inventory data."
    
    summary = {
        "total_products": all_products['total_products'],
        "expired_products": expired['total_products'],
        "expiring_this_week": expiring_week['total_products'],
        "healthy_products": all_products['total_products'] - expiring_week['total_products']
    }
    
    return summary
```

## Configuration

### Environment Variables

For development and testing:

```bash
export FRESH_ALERT_BEARER_TOKEN="your-bearer-token"
export FRESH_ALERT_BASE_URL="https://api.freshalert.com"  # Optional
```

### Production Usage

In production (especially with LangGraph), pass tokens dynamically:

```python
# ✅ Recommended: Pass token from request headers
token = extract_token_from_headers(request)
result = await fresh_alert_get_user_products(token)

# ❌ Avoid: Hardcoded tokens in production
result = await fresh_alert_get_user_products("hardcoded-token")
```

## Logging

Enable debug logging to troubleshoot issues:

```python
import logging

# Enable Fresh Alert MCP logging
logging.getLogger("fresh_alert_mcp").setLevel(logging.DEBUG)

# Enable Fresh Alert client logging
logging.getLogger("src.utils.freshalert").setLevel(logging.DEBUG)
```

## Contributing

To extend the MCP tools:

1. Add new methods to the `FreshAlertTools` class
2. Create corresponding standalone functions
3. Add comprehensive tests
4. Update documentation

## License

This MCP tool is part of the Fresh Alert Agent project.