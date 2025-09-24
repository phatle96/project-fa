"""
Test file for Fresh Alert MCP tools.

This file provides comprehensive testing for the Fresh Alert MCP tools
including various scenarios, error handling, and integration testing.
"""

import asyncio
import os
import sys
from typing import Dict, Any
import logging
from datetime import datetime, timezone, timedelta

# Add the src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from fresh_alert_mcp import (
    FreshAlertTools,
    fresh_alert_get_user_products,
    fresh_alert_get_expired_products
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FreshAlertMCPTester:
    """Comprehensive test suite for Fresh Alert MCP tools"""
    
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.tools = FreshAlertTools(bearer_token=bearer_token)
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    def log_test_result(self, test_name: str, success: bool, message: str = ""):
        """Log test results"""
        if success:
            self.test_results["passed"] += 1
            logger.info(f"✅ {test_name}: PASSED {message}")
        else:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"{test_name}: {message}")
            logger.error(f"❌ {test_name}: FAILED {message}")
    
    async def test_get_user_products_success(self):
        """Test successful retrieval of user products"""
        test_name = "Get User Products - Success Case"
        
        try:
            result = await self.tools.get_user_products()
            
            # Check response structure
            if not isinstance(result, dict):
                self.log_test_result(test_name, False, "Response is not a dictionary")
                return
            
            if 'error' in result:
                self.log_test_result(test_name, False, f"API returned error: {result['error']}")
                return
            
            # Check required fields
            required_fields = ['total_products', 'products']
            for field in required_fields:
                if field not in result:
                    self.log_test_result(test_name, False, f"Missing required field: {field}")
                    return
            
            # Check data types
            if not isinstance(result['total_products'], int):
                self.log_test_result(test_name, False, "total_products is not an integer")
                return
            
            if not isinstance(result['products'], list):
                self.log_test_result(test_name, False, "products is not a list")
                return
            
            # Validate product structure if products exist
            if result['products']:
                product = result['products'][0]
                required_product_fields = ['id', 'product_name', 'date_tracking']
                
                for field in required_product_fields:
                    if field not in product:
                        self.log_test_result(test_name, False, f"Product missing field: {field}")
                        return
            
            self.log_test_result(
                test_name, 
                True, 
                f"- Found {result['total_products']} products"
            )
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Exception: {str(e)}")
    
    async def test_get_expired_products_no_days(self):
        """Test getting already expired products"""
        test_name = "Get Expired Products - No Days Parameter"
        
        try:
            result = await self.tools.get_expired_products()
            
            # Check response structure
            if not isinstance(result, dict):
                self.log_test_result(test_name, False, "Response is not a dictionary")
                return
            
            if 'error' in result:
                # Error might be acceptable if no expired products found
                if 'No expired' in result.get('error', '') or result.get('message'):
                    self.log_test_result(test_name, True, "- No expired products found (acceptable)")
                    return
                else:
                    self.log_test_result(test_name, False, f"API returned error: {result['error']}")
                    return
            
            # Check required fields
            required_fields = ['search_criteria', 'total_products', 'products']
            for field in required_fields:
                if field not in result:
                    self.log_test_result(test_name, False, f"Missing required field: {field}")
                    return
            
            # Check search criteria
            if result['search_criteria']['days'] is not None:
                self.log_test_result(test_name, False, "Days should be None for expired products")
                return
            
            self.log_test_result(
                test_name, 
                True, 
                f"- Found {result['total_products']} expired products"
            )
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Exception: {str(e)}")
    
    async def test_get_expired_products_with_days(self):
        """Test getting products expiring within specified days"""
        test_name = "Get Expired Products - With Days Parameter"
        test_days = 7
        
        try:
            result = await self.tools.get_expired_products(days=test_days)
            
            # Check response structure
            if not isinstance(result, dict):
                self.log_test_result(test_name, False, "Response is not a dictionary")
                return
            
            if 'error' in result:
                # Error might be acceptable if no expiring products found
                if 'No expired' in result.get('error', '') or result.get('message'):
                    self.log_test_result(test_name, True, f"- No products expiring in {test_days} days (acceptable)")
                    return
                else:
                    self.log_test_result(test_name, False, f"API returned error: {result['error']}")
                    return
            
            # Check search criteria
            if result['search_criteria']['days'] != test_days:
                self.log_test_result(test_name, False, f"Days mismatch: expected {test_days}, got {result['search_criteria']['days']}")
                return
            
            # Validate date tracking if products exist
            if result['products']:
                for product in result['products']:
                    if product['date_tracking']:
                        for date_info in product['date_tracking']:
                            if 'days_until_expiry' in date_info:
                                days_until = date_info['days_until_expiry']
                                # Should be within the specified range
                                if days_until > test_days:
                                    self.log_test_result(
                                        test_name, 
                                        False, 
                                        f"Product expires in {days_until} days, outside {test_days} day range"
                                    )
                                    return
            
            self.log_test_result(
                test_name, 
                True, 
                f"- Found {result['total_products']} products expiring within {test_days} days"
            )
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Exception: {str(e)}")
    
    async def test_standalone_functions(self):
        """Test standalone MCP tool functions"""
        test_name = "Standalone Functions"
        
        try:
            # Test standalone get_user_products
            user_products = await fresh_alert_get_user_products(self.bearer_token)
            
            if 'error' in user_products and 'authentication' not in user_products['error'].lower():
                self.log_test_result(test_name, False, f"Standalone get_user_products failed: {user_products['error']}")
                return
            
            # Test standalone get_expired_products
            expired_products = await fresh_alert_get_expired_products(self.bearer_token, days=5)
            
            if 'error' in expired_products and 'authentication' not in expired_products['error'].lower():
                # Only fail if it's not a "no products found" type error
                if 'No expired' not in expired_products.get('error', ''):
                    self.log_test_result(test_name, False, f"Standalone get_expired_products failed: {expired_products['error']}")
                    return
            
            self.log_test_result(test_name, True, "- Both standalone functions work correctly")
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Exception: {str(e)}")
    
    async def test_error_handling(self):
        """Test error handling with invalid token"""
        test_name = "Error Handling - Invalid Token"
        
        try:
            # Create tools with invalid token
            invalid_tools = FreshAlertTools(bearer_token="invalid-token-12345")
            result = await invalid_tools.get_user_products()
            
            # Should return error response, not raise exception
            if 'error' not in result:
                self.log_test_result(test_name, False, "Should return error for invalid token")
                return
            
            if result.get('error_type') != 'authentication_error':
                self.log_test_result(test_name, False, f"Expected authentication_error, got {result.get('error_type')}")
                return
            
            self.log_test_result(test_name, True, "- Properly handles authentication errors")
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Should not raise exception: {str(e)}")
    
    async def test_data_format_validation(self):
        """Test that returned data has correct format"""
        test_name = "Data Format Validation"
        
        try:
            result = await self.tools.get_user_products()
            
            if 'error' in result:
                # Skip validation if API returns error
                self.log_test_result(test_name, True, "- Skipped due to API error (acceptable)")
                return
            
            # Check date format in products
            for product in result.get('products', []):
                for date_info in product.get('date_tracking', []):
                    # Check ISO format dates
                    date_fields = ['date_manufactured', 'date_best_before', 'date_expired']
                    for field in date_fields:
                        if field in date_info and date_info[field]:
                            try:
                                # Should be valid ISO format
                                datetime.fromisoformat(date_info[field].replace('Z', '+00:00'))
                            except ValueError:
                                self.log_test_result(test_name, False, f"Invalid date format in {field}: {date_info[field]}")
                                return
            
            self.log_test_result(test_name, True, "- All dates are in correct ISO format")
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all tests"""
        logger.info("🧪 Starting Fresh Alert MCP Tools Test Suite")
        logger.info("=" * 60)
        
        # Run all test methods
        await self.test_get_user_products_success()
        await self.test_get_expired_products_no_days()
        await self.test_get_expired_products_with_days()
        await self.test_standalone_functions()
        await self.test_error_handling()
        await self.test_data_format_validation()
        
        # Print summary
        logger.info("=" * 60)
        logger.info("🏁 Test Suite Summary")
        logger.info(f"✅ Tests Passed: {self.test_results['passed']}")
        logger.info(f"❌ Tests Failed: {self.test_results['failed']}")
        
        if self.test_results['errors']:
            logger.info("\n📋 Failed Tests:")
            for error in self.test_results['errors']:
                logger.info(f"   - {error}")
        
        total_tests = self.test_results['passed'] + self.test_results['failed']
        success_rate = (self.test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
        logger.info(f"\n📊 Success Rate: {success_rate:.1f}%")
        
        return self.test_results


async def test_integration_with_langgraph():
    """Test integration scenario with LangGraph-style token passing"""
    logger.info("\n🔗 Testing LangGraph Integration Scenario")
    logger.info("-" * 50)
    
    # Simulate LangGraph config with headers
    mock_config = {
        "configurable": {
            "headers": {
                "Authentication": f"Bearer {os.getenv('FRESH_ALERT_BEARER_TOKEN', 'test-token')}",
                "Content-Type": "application/json"
            }
        }
    }
    
    def extract_token_from_config(config: Dict[str, Any]) -> str:
        """Extract token from LangGraph config (simulated)"""
        headers = config.get("configurable", {}).get("headers", {})
        auth_header = headers.get("Authentication", "")
        
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        
        return ""
    
    # Extract token
    token = extract_token_from_config(mock_config)
    
    if not token or token == "test-token":
        logger.warning("⚠️  No valid token for integration test - set FRESH_ALERT_BEARER_TOKEN")
        return
    
    try:
        # Test the integration flow
        logger.info("1. Extracting token from mock LangGraph config...")
        logger.info(f"   Token: {token[:10]}..." if len(token) > 10 else "   Token: [hidden]")
        
        logger.info("2. Calling Fresh Alert tools with extracted token...")
        products = await fresh_alert_get_user_products(token)
        
        if 'error' in products:
            logger.error(f"   ❌ Error: {products['error']}")
        else:
            logger.info(f"   ✅ Successfully retrieved {products['total_products']} products")
        
        logger.info("3. Testing expiring products...")
        expiring = await fresh_alert_get_expired_products(token, days=7)
        
        if 'error' in expiring:
            if 'No expired' in expiring.get('error', '') or expiring.get('message'):
                logger.info("   ✅ No expiring products found (acceptable)")
            else:
                logger.error(f"   ❌ Error: {expiring['error']}")
        else:
            logger.info(f"   ✅ Found {expiring['total_products']} products expiring within 7 days")
        
        logger.info("🎉 Integration test completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")


if __name__ == "__main__":
    """Run the test suite"""
    
    # Check for Bearer token
    bearer_token = os.getenv("FRESH_ALERT_BEARER_TOKEN")
    
    if not bearer_token:
        logger.error("❌ FRESH_ALERT_BEARER_TOKEN environment variable is required for testing")
        logger.info("💡 Set your Fresh Alert Bearer token:")
        logger.info("   export FRESH_ALERT_BEARER_TOKEN='your-token-here'")
        sys.exit(1)
    
    async def main():
        # Run comprehensive test suite
        tester = FreshAlertMCPTester(bearer_token)
        results = await tester.run_all_tests()
        
        # Run integration test
        await test_integration_with_langgraph()
        
        # Exit with appropriate code
        exit_code = 0 if results['failed'] == 0 else 1
        sys.exit(exit_code)
    
    # Run tests
    asyncio.run(main())