# Spoonacular API Client

A modular, async-first Python client for the Spoonacular API with clean separation of concerns, comprehensive error handling, and both async and sync interfaces.

## Features

- **Modular Architecture**: Clean separation between models, API endpoints, configuration, and HTTP client
- **Async First**: Built with async/await from the ground up, with sync wrapper for convenience
- **Comprehensive Models**: Full Pydantic models with validation for requests and responses
- **Error Handling**: Detailed exception hierarchy with proper error context
- **Type Safety**: Full type hints and validation throughout
- **Retry Logic**: Built-in retry mechanisms with exponential backoff
- **Rate Limiting**: Automatic rate limiting to respect API limits
- **Flexible Configuration**: Environment variable support with override capabilities

## Installation

```bash
pip install httpx pydantic pydantic-settings
```

## Quick Start

### Async Usage (Recommended)

```python
from utils.spoonacular import SpoonacularClient

async def main():
    async with SpoonacularClient(api_key="your-api-key") as client:
        recipes_api = await client.recipes
        
        # Search for recipes
        results = await recipes_api.complex_search(
            query="pasta",
            cuisine="italian",
            number=10
        )
        
        # Get detailed recipe information
        if results.results:
            recipe = await recipes_api.get_recipe_information(
                recipe_id=results.results[0].id,
                include_nutrition=True
            )
            print(f"Recipe: {recipe.title}")

import asyncio
asyncio.run(main())
```

### Sync Usage

```python
from utils.spoonacular import create_client

# Create client
client = create_client(api_key="your-api-key")

# Search for recipes
results = client.sync.recipes.complex_search(
    query="chicken curry",
    cuisine="indian",
    max_ready_time=45
)

# Get recipe details
if results.results:
    recipe = client.sync.recipes.get_recipe_information(
        recipe_id=results.results[0].id
    )
    print(f"Recipe: {recipe.title}")
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
SPOONACULAR_API_KEY=your-api-key-here
SPOONACULAR_BASE_URL=https://api.spoonacular.com
SPOONACULAR_TIMEOUT=30
SPOONACULAR_MAX_RETRIES=3
```

### Programmatic Configuration

```python
from utils.spoonacular import SpoonacularClient, SpoonacularConfig

config = SpoonacularConfig(
    api_key="your-api-key",
    timeout=30,
    max_retries=3,
    rate_limit_calls=150,
    rate_limit_period=60
)

client = SpoonacularClient(config=config)
```

## API Reference

### Complex Search

Search for recipes with advanced filtering:

```python
from utils.spoonacular import ComplexSearchRequest, Cuisine, Diet

# Using request object
search_request = ComplexSearchRequest(
    query="pasta",
    cuisine=[Cuisine.ITALIAN],
    diet=[Diet.VEGETARIAN],
    max_ready_time=30,
    min_protein=20,
    number=20,
    add_recipe_information=True
)

results = await recipes_api.complex_search(search_request)

# Using individual parameters
results = await recipes_api.complex_search(
    query="chicken curry",
    cuisine="indian",
    exclude_ingredients=["nuts", "dairy"],
    max_ready_time=45
)
```

### Recipe Information

Get detailed information about a specific recipe:

```python
recipe = await recipes_api.get_recipe_information(
    recipe_id=1096211,
    include_nutrition=True,
    add_wine_pairing=True,
    add_taste_data=True
)

print(f"Title: {recipe.title}")
print(f"Ready in: {recipe.ready_in_minutes} minutes")
print(f"Servings: {recipe.servings}")

if recipe.nutrition:
    for nutrient in recipe.nutrition.nutrients:
        print(f"{nutrient.name}: {nutrient.amount} {nutrient.unit}")
```

### Similar Recipes

Find recipes similar to a given recipe:

```python
similar = await recipes_api.get_similar_recipes(
    recipe_id=1096211,
    number=5
)

for recipe in similar.recipes:
    print(f"- {recipe.title}")
```

### Random Recipes

Get random recipes with optional filtering:

```python
random_recipes = await recipes_api.get_random_recipes(
    number=10,
    include_tags=["vegetarian", "healthy"],
    exclude_tags=["dairy"]
)

for recipe in random_recipes.recipes:
    print(f"- {recipe.title}")
```

### Autocomplete

Get recipe suggestions for partial queries:

```python
suggestions = await recipes_api.autocomplete_recipe_search(
    query="choc",
    number=10
)

for suggestion in suggestions.suggestions:
    print(f"- {suggestion.title}")
```

## Advanced Usage

### Custom Search Parameters

The client supports all Spoonacular API parameters:

```python
results = await recipes_api.complex_search(
    # Basic search
    query="pasta",
    
    # Cuisine and diet
    cuisine=["italian", "mediterranean"],
    diet=["vegetarian"],
    intolerances=["dairy", "gluten"],
    
    # Ingredients
    include_ingredients=["tomato", "basil"],
    exclude_ingredients=["meat", "fish"],
    
    # Nutritional constraints
    min_carbs=30,
    max_carbs=100,
    min_protein=20,
    max_calories=500,
    
    # Time and complexity
    max_ready_time=45,
    min_ready_time=15,
    
    # Result options
    number=20,
    offset=0,
    sort="popularity",
    sort_direction="desc",
    add_recipe_information=True,
    add_recipe_nutrition=True,
    
    # Other options
    fill_ingredients=True,
    instructions_required=True,
    limit_license=True
)
```

### Error Handling

The client provides specific exception types:

```python
from utils.spoonacular import (
    SpoonacularException,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError
)

try:
    results = await recipes_api.complex_search(query="pasta")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded")
except NotFoundError:
    print("Recipe not found")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except SpoonacularException as e:
    print(f"API error: {e}")
```

### Request Validation

Use request objects for better validation:

```python
from utils.spoonacular import ComplexSearchRequest

# This will validate parameters at creation time
request = ComplexSearchRequest(
    query="pasta",
    number=20,  # Valid range: 1-100
    offset=0,   # Must be >= 0
    max_ready_time=45  # Must be > 0
)

# Execute the validated request
results = await request.execute(recipes_api)
```

## Project Structure

```
utils/spoonacular/
├── __init__.py              # Main exports
├── client.py               # Main client classes
├── config.py               # Configuration management
├── exceptions.py           # Exception hierarchy
├── base_client.py          # HTTP client with retry/rate limiting
├── api/
│   ├── __init__.py
│   └── recipes.py          # Recipes API implementation
└── models/
    ├── __init__.py         # Model exports
    ├── enums.py           # Enumerations (cuisines, diets, etc.)
    ├── common.py          # Common model components
    ├── requests.py        # Request models
    └── responses.py       # Response models
```

## Model Reference

### Enums

- `Cuisine`: Italian, Indian, Chinese, etc.
- `Diet`: Vegetarian, Vegan, Gluten Free, etc.
- `Intolerance`: Dairy, Egg, Gluten, etc.
- `MealType`: Main Course, Side Dish, Dessert, etc.
- `RecipeSort`: Popularity, Healthiness, Price, Time, etc.

### Request Models

- `ComplexSearchRequest`: Parameters for complex recipe search
- `RecipeInformationRequest`: Parameters for recipe details

### Response Models

- `ComplexSearchResponse`: Search results with pagination
- `Recipe`: Detailed recipe information
- `RecipeSearchResult`: Basic recipe information from search
- `SimilarRecipesResponse`: Similar recipe results
- `RandomRecipesResponse`: Random recipe results
- `AutocompleteResponse`: Autocomplete suggestions

### Common Models

- `Ingredient`: Recipe ingredient with measurements
- `Equipment`: Required cooking equipment
- `Instruction`: Step-by-step cooking instructions
- `NutritionInfo`: Nutritional information and analysis

## Testing

Run the test suite:

```bash
# Run all tests
python test_spoonacular_client.py

# Run with pytest for more options
pip install pytest
pytest test_spoonacular_client.py -v

# Run integration tests (requires API key)
SPOONACULAR_API_KEY=your-key pytest test_spoonacular_client.py::TestIntegration -v
```

## Examples

See `spoonacular_examples.py` for comprehensive usage examples including:

- Basic and advanced search patterns
- Async and sync usage
- Error handling
- Nutrient-based filtering
- Ingredient inclusion/exclusion
- Multiple dietary restrictions

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## API Key

Get your free API key from [Spoonacular](https://spoonacular.com/food-api) to get started.