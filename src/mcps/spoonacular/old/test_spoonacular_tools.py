"""
Test script for Spoonacular agent tools.

This script tests both the async and sync versions of the agent tools
to ensure they work correctly with the modular Spoonacular client.
"""

import os
import sys
import asyncio

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcps.spoonacular_agent_tools import (
    search_recipes,
    get_recipe_details,
    search_recipes_sync,
    get_recipe_details_sync
)


async def test_async_tools():
    """Test the async version of the tools"""
    print("🔄 Testing Async Tools")
    print("=" * 40)
    
    # Test 1: Basic search
    print("1. Testing basic recipe search...")
    result = await search_recipes(
        query="pasta carbonara",
        number=3
    )
    print(result)
    print()
    
    # Test 2: Advanced search with constraints
    print("2. Testing advanced search with dietary constraints...")
    result = await search_recipes(
        query="chicken curry",
        cuisine="indian",
        diet="gluten free",
        max_ready_time=45,
        number=2
    )
    print(result)
    print()
    
    # Test 3: Ingredient-based search
    print("3. Testing ingredient-based search...")
    result = await search_recipes(
        query="salad",
        include_ingredients="tomato, cucumber",
        exclude_ingredients="nuts, dairy",
        number=2
    )
    print(result)
    print()
    
    # Test 4: Get recipe details (using a known recipe ID)
    print("4. Testing recipe details retrieval...")
    # Using a common recipe ID that should exist
    result = await get_recipe_details(
        recipe_id=1096211,  # A recipe that typically exists
        include_nutrition=True
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    print()


def test_sync_tools():
    """Test the sync version of the tools"""
    print("🔄 Testing Sync Tools")
    print("=" * 40)
    
    # Test 1: Sync search
    print("1. Testing sync recipe search...")
    result = search_recipes_sync(
        query="chocolate cake",
        number=2
    )
    print(result)
    print()
    
    # Test 2: Sync recipe details
    print("2. Testing sync recipe details...")
    result = get_recipe_details_sync(
        recipe_id=1096211,
        include_nutrition=False
    )
    print(result[:300] + "..." if len(result) > 300 else result)
    print()


def test_error_handling():
    """Test error handling scenarios"""
    print("🔄 Testing Error Handling")
    print("=" * 40)
    
    # Test with no API key (temporarily remove it)
    original_key = os.environ.get("SPOONACULAR_API_KEY")
    if original_key:
        del os.environ["SPOONACULAR_API_KEY"]
    
    print("1. Testing with missing API key...")
    result = search_recipes_sync("pasta", number=1)
    print(result)
    
    # Restore API key
    if original_key:
        os.environ["SPOONACULAR_API_KEY"] = original_key
    
    print()
    
    # Test with invalid recipe ID
    print("2. Testing with invalid recipe ID...")
    result = get_recipe_details_sync(999999999)
    print(result)
    print()


async def main():
    """Run all tests"""
    print("Spoonacular Agent Tools Test Suite")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        print("⚠️  SPOONACULAR_API_KEY not set - will test error handling only")
        test_error_handling()
        return
    
    print(f"✅ Using API key: {api_key[:10]}...")
    print()
    
    try:
        # Test async tools
        await test_async_tools()
        
        print("✅ All async tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


def main_sync():
    """Run sync tests separately"""
    print("Spoonacular Agent Tools - Sync Test Suite")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        print("⚠️  SPOONACULAR_API_KEY not set")
        return
    
    print(f"✅ Using API key: {api_key[:10]}...")
    print()
    
    try:
        # Test sync tools
        test_sync_tools()
        
        # Test error handling
        test_error_handling()
        
        print("✅ All sync tests completed!")
        
    except Exception as e:
        print(f"❌ Sync test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        # Run sync tests only
        main_sync()
    else:
        # Run async tests
        asyncio.run(main())