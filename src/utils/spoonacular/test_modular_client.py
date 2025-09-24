"""
Quick test script for the new modular Spoonacular client.
"""

import asyncio
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from spoonacular import SpoonacularClient, ComplexSearchRequest, Cuisine, Diet


async def test_client():
    """Test the basic functionality of the client"""
    
    # Check if API key is available
    api_key = os.getenv("SPOONACULAR_API_KEY", "test-api-key")
    print(f"Using API key: {api_key[:10]}..." if len(api_key) > 10 else "No API key")
    
    try:
        # Test client creation
        print("1. Creating client...")
        async with SpoonacularClient(api_key=api_key) as client:
            print("✓ Client created successfully")
            
            # Test recipes API access
            print("2. Getting recipes API...")
            recipes_api = await client.recipes
            print("✓ Recipes API accessible")
            
            # Test model creation
            print("3. Creating search request...")
            search_request = ComplexSearchRequest(
                query="pasta",
                cuisine=[Cuisine.ITALIAN],
                diet=[Diet.VEGETARIAN],
                number=5
            )
            print("✓ Search request created")
            
            # Test parameter conversion
            print("4. Testing parameter conversion...")
            params = search_request.model_dump(exclude_none=True)
            api_params = recipes_api._convert_search_params(params)
            print(f"✓ Parameters converted: {api_params}")
            
            print("\n✅ All basic tests passed!")
            
            # If we have a real API key, try a real request
            if api_key != "test-api-key" and len(api_key) > 10:
                print("\n5. Testing real API call...")
                try:
                    results = await recipes_api.complex_search(
                        query="pasta",
                        number=2
                    )
                    print(f"✓ API call successful! Found {results.total_results} recipes")
                    if results.results:
                        print(f"   First recipe: {results.results[0].title}")
                except Exception as e:
                    print(f"⚠ API call failed (expected if using test key): {e}")
            else:
                print("\n5. Skipping real API call (no valid API key)")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


def test_sync_client():
    """Test synchronous client"""
    
    api_key = os.getenv("SPOONACULAR_API_KEY", "test-api-key")
    
    try:
        print("\n6. Testing sync client...")
        from spoonacular import create_client
        
        client = create_client(api_key=api_key)
        print("✓ Sync client created")
        
        # Test sync access
        sync_recipes = client.sync.recipes
        print("✓ Sync recipes API accessible")
        
        print("✅ Sync client tests passed!")
        
    except Exception as e:
        print(f"❌ Sync test failed: {e}")
        raise


if __name__ == "__main__":
    print("Testing Modular Spoonacular Client")
    print("=" * 40)
    
    # Run async tests
    asyncio.run(test_client())
    
    # Run sync tests
    test_sync_client()
    
    print("\n🎉 All tests completed successfully!")