"""
Example usage of Fresh Alert MCP tools.

This example demonstrates how to use the Fresh Alert MCP tools in various scenarios
including LangGraph integration, error handling, and practical use cases.
"""

import asyncio
import os
import logging
from typing import Dict, Any

from fresh_alert_mcp import (
    FreshAlertTools,
    fresh_alert_get_user_products,
    fresh_alert_get_expired_products
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def basic_usage_example():
    """Basic usage of Fresh Alert MCP tools"""
    logger.info("🍎 Fresh Alert MCP Tools - Basic Usage Example")
    logger.info("=" * 50)
    
    # Get Bearer token (in real usage, this comes from request headers)
    bearer_token = os.getenv("FRESH_ALERT_BEARER_TOKEN")
    
    if not bearer_token:
        logger.warning("⚠️  Set FRESH_ALERT_BEARER_TOKEN environment variable to run examples")
        return
    
    try:
        # Example 1: Get all user products
        logger.info("📦 Getting all user products...")
        products = await fresh_alert_get_user_products(bearer_token)
        
        if 'error' in products:
            logger.error(f"❌ Error: {products['error']}")
        else:
            logger.info(f"✅ Found {products['total_products']} products")
            
            # Show some product details
            for i, product in enumerate(products['products'][:3], 1):
                name = product['product_name'] or 'Unknown Product'
                brand = product['brand'] or 'Unknown Brand'
                logger.info(f"   {i}. {name} ({brand})")
        
        # Example 2: Get expired products
        logger.info("\n⏰ Getting already expired products...")
        expired = await fresh_alert_get_expired_products(bearer_token)
        
        if 'error' in expired:
            if 'No expired' in expired.get('error', '') or expired.get('message'):
                logger.info("✅ No expired products found (good news!)")
            else:
                logger.error(f"❌ Error: {expired['error']}")
        else:
            logger.info(f"⚠️  Found {expired['total_products']} expired products")
        
        # Example 3: Get products expiring soon
        logger.info("\n📅 Getting products expiring in next 7 days...")
        expiring = await fresh_alert_get_expired_products(bearer_token, days=7)
        
        if 'error' in expiring:
            if 'No expired' in expiring.get('error', '') or expiring.get('message'):
                logger.info("✅ No products expiring in the next 7 days")
            else:
                logger.error(f"❌ Error: {expiring['error']}")
        else:
            logger.info(f"📍 Found {expiring['total_products']} products expiring within 7 days")
            
            # Show expiration details
            for product in expiring['products'][:3]:
                name = product['product_name'] or 'Unknown Product'
                for date_info in product['date_tracking']:
                    if 'days_until_expiry' in date_info:
                        days = date_info['days_until_expiry']
                        if days >= 0:
                            logger.info(f"   - {name}: expires in {days} days")
    
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")


async def langgraph_integration_example():
    """Example of LangGraph integration"""
    logger.info("\n🔗 LangGraph Integration Example")
    logger.info("=" * 40)
    
    # Simulate LangGraph config with headers
    mock_config = {
        "configurable": {
            "headers": {
                "Authentication": f"Bearer {os.getenv('FRESH_ALERT_BEARER_TOKEN', 'test-token')}",
                "Content-Type": "application/json",
                "User-Agent": "LangGraph-Agent/1.0"
            }
        }
    }
    
    def extract_token_from_config(config: Dict[str, Any]) -> str:
        """Extract Bearer token from LangGraph config"""
        headers = config.get("configurable", {}).get("headers", {})
        auth_header = headers.get("Authentication", "")
        
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        
        raise ValueError("No valid Bearer token found in request headers")
    
    async def food_assistant_agent(config: Dict[str, Any], user_query: str) -> str:
        """Simulated LangGraph agent using Fresh Alert tools"""
        try:
            # Extract token from request headers
            token = extract_token_from_config(config)
            
            logger.info(f"🤖 Processing query: '{user_query}'")
            logger.info(f"🔐 Using token: {token[:10]}..." if len(token) > 10 else "🔐 Using token: [hidden]")
            
            # Use Fresh Alert tools based on query
            if "expired" in user_query.lower() or "expir" in user_query.lower():
                # Query about expiring products
                result = await fresh_alert_get_expired_products(token, days=7)
                
                if 'error' in result:
                    return f"Sorry, I couldn't check your expiring products: {result['error']}"
                
                if result['total_products'] == 0:
                    return "Good news! You don't have any products expiring in the next 7 days."
                
                response = f"You have {result['total_products']} products expiring within 7 days:\n"
                for product in result['products'][:5]:  # Show first 5
                    name = product['product_name'] or 'Unknown Product'
                    for date_info in product['date_tracking']:
                        if 'days_until_expiry' in date_info and date_info['days_until_expiry'] >= 0:
                            days = date_info['days_until_expiry']
                            response += f"- {name}: expires in {days} days\n"
                
                return response.strip()
            
            else:
                # General query about products
                result = await fresh_alert_get_user_products(token)
                
                if 'error' in result:
                    return f"Sorry, I couldn't access your products: {result['error']}"
                
                return f"You have {result['total_products']} products in your Fresh Alert account."
        
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    # Test the agent with different queries
    test_queries = [
        "What products do I have?",
        "Show me what's expiring soon",
        "Do I have any expired food?"
    ]
    
    for query in test_queries:
        try:
            response = await food_assistant_agent(mock_config, query)
            logger.info(f"🤖 Query: {query}")
            logger.info(f"📝 Response: {response}\n")
        except Exception as e:
            logger.error(f"❌ Error processing query '{query}': {e}\n")


async def practical_use_cases():
    """Demonstrate practical use cases"""
    logger.info("\n🍽️  Practical Use Cases")
    logger.info("=" * 30)
    
    bearer_token = os.getenv("FRESH_ALERT_BEARER_TOKEN")
    
    if not bearer_token:
        logger.warning("⚠️  Set FRESH_ALERT_BEARER_TOKEN to run practical examples")
        return
    
    # Use Case 1: Meal Planning Assistant
    async def meal_planning_assistant():
        logger.info("👨‍🍳 Use Case 1: Meal Planning Assistant")
        
        expiring = await fresh_alert_get_expired_products(bearer_token, days=3)
        
        if 'error' in expiring:
            return "Unable to check your expiring products for meal planning."
        
        if expiring['total_products'] == 0:
            return "✅ No products expiring in the next 3 days. You're all set!"
        
        suggestions = []
        for product in expiring['products']:
            name = product['product_name'] or 'Unknown Product'
            category = product.get('category') or 'Unknown'
            
            for date_info in product['date_tracking']:
                if 'days_until_expiry' in date_info and date_info['days_until_expiry'] <= 3:
                    days = date_info['days_until_expiry']
                    if days == 0:
                        suggestions.append(f"🚨 {name} ({category}) - expires TODAY!")
                    elif days == 1:
                        suggestions.append(f"⚠️  {name} ({category}) - expires tomorrow")
                    else:
                        suggestions.append(f"📅 {name} ({category}) - expires in {days} days")
        
        if suggestions:
            return "Consider using these ingredients soon:\n" + "\n".join(suggestions)
        else:
            return "✅ No products need immediate attention."
    
    # Use Case 2: Food Waste Prevention
    async def food_waste_checker():
        logger.info("\n🗑️  Use Case 2: Food Waste Prevention")
        
        expired = await fresh_alert_get_expired_products(bearer_token)
        expiring_today = await fresh_alert_get_expired_products(bearer_token, days=0)
        
        alerts = []
        
        if not 'error' in expired and expired['total_products'] > 0:
            alerts.append(f"⚠️  {expired['total_products']} products have already expired")
        
        if not 'error' in expiring_today and expiring_today['total_products'] > 0:
            alerts.append(f"🚨 {expiring_today['total_products']} products expire today")
        
        if alerts:
            return "Food waste alerts:\n" + "\n".join(alerts)
        else:
            return "✅ No immediate food waste concerns"
    
    # Use Case 3: Inventory Summary
    async def inventory_summary():
        logger.info("\n📊 Use Case 3: Inventory Summary")
        
        all_products = await fresh_alert_get_user_products(bearer_token)
        expired = await fresh_alert_get_expired_products(bearer_token)
        expiring_week = await fresh_alert_get_expired_products(bearer_token, days=7)
        
        if any('error' in result for result in [all_products, expired, expiring_week]):
            return "Unable to generate inventory summary"
        
        total = all_products['total_products']
        expired_count = expired['total_products'] if 'total_products' in expired else 0
        expiring_count = expiring_week['total_products'] if 'total_products' in expiring_week else 0
        healthy_count = total - expiring_count
        
        return f"""📈 Inventory Summary:
   📦 Total products: {total}
   ✅ Healthy products: {healthy_count}
   📅 Expiring this week: {expiring_count}
   ⚠️  Already expired: {expired_count}"""
    
    # Run use cases
    try:
        meal_result = await meal_planning_assistant()
        logger.info(f"📝 {meal_result}\n")
        
        waste_result = await food_waste_checker()
        logger.info(f"📝 {waste_result}\n")
        
        summary_result = await inventory_summary()
        logger.info(f"📝 {summary_result}")
        
    except Exception as e:
        logger.error(f"❌ Error in practical use cases: {e}")


async def error_handling_example():
    """Demonstrate error handling"""
    logger.info("\n🛡️  Error Handling Example")
    logger.info("=" * 35)
    
    # Test with invalid token
    logger.info("🧪 Testing with invalid token...")
    try:
        result = await fresh_alert_get_user_products("invalid-token-12345")
        
        if 'error' in result:
            error_type = result.get('error_type', 'unknown')
            logger.info(f"✅ Properly handled {error_type}: {result['error']}")
        else:
            logger.warning("⚠️  Expected error but got success")
    
    except Exception as e:
        logger.error(f"❌ Unexpected exception: {e}")
    
    # Test with None token
    logger.info("\n🧪 Testing with None token...")
    try:
        tools = FreshAlertTools(bearer_token=None)
        logger.warning("⚠️  Expected ValueError but got success")
    except ValueError as e:
        logger.info(f"✅ Properly handled missing token: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected exception: {e}")


if __name__ == "__main__":
    """Run all examples"""
    
    async def main():
        await basic_usage_example()
        await langgraph_integration_example()
        await practical_use_cases()
        await error_handling_example()
        
        logger.info("\n🎉 All examples completed!")
    
    # Run examples
    asyncio.run(main())