# Spoonacular Agent Tools

This module provides easy-to-use tools for AI agents to search recipes and retrieve detailed recipe information using the Spoonacular API through our modular client.

## Overview

The Spoonacular agent tools offer two main functions:

1. **Recipe Search** - Find recipes based on natural language queries, dietary restrictions, cuisine preferences, and time constraints
2. **Recipe Details** - Get comprehensive information about specific recipes including ingredients, instructions, and nutrition

## Quick Start

### Setup

```bash
# Set your Spoonacular API key
export SPOONACULAR_API_KEY="your-api-key-here"
```

### Basic Usage

```python
import asyncio
from mcps.spoonacular_agent_tools import search_recipes, get_recipe_details

async def example():
    # Search for recipes
    results = await search_recipes(
        query="pasta carbonara",
        number=3
    )
    print(results)
    
    # Get detailed recipe information
    details = await get_recipe_details(
        recipe_id=1096211,
        include_nutrition=True
    )
    print(details)

asyncio.run(example())
```

## API Reference

### search_recipes()

Search for recipes using natural language parameters.

```python
async def search_recipes(
    query: str,
    cuisine: Optional[str] = None,
    diet: Optional[str] = None,
    max_ready_time: Optional[int] = None,
    include_ingredients: Optional[str] = None,
    exclude_ingredients: Optional[str] = None,
    number: int = 10
) -> str
```

**Parameters:**
- `query` (str): What to search for (e.g., "pasta", "chicken curry")
- `cuisine` (str, optional): Type of cuisine (e.g., "italian", "indian", "mexican")
- `diet` (str, optional): Dietary restriction (e.g., "vegetarian", "vegan", "gluten free")
- `max_ready_time` (int, optional): Maximum cooking time in minutes
- `include_ingredients` (str, optional): Comma-separated ingredients that must be included
- `exclude_ingredients` (str, optional): Comma-separated ingredients to avoid
- `number` (int): Number of recipes to return (1-20, default: 10)

**Returns:**
- Formatted string with recipe search results including titles, cooking times, dietary tags, and IDs

**Examples:**

```python
# Basic search
results = await search_recipes(query="pasta", number=5)

# Advanced search with constraints
results = await search_recipes(
    query="chicken curry",
    cuisine="indian",
    diet="gluten free",
    max_ready_time=45,
    number=10
)

# Ingredient-based search
results = await search_recipes(
    query="salad",
    include_ingredients="tomato, cucumber",
    exclude_ingredients="nuts, dairy",
    number=5
)
```

### get_recipe_details()

Get detailed information about a specific recipe.

```python
async def get_recipe_details(
    recipe_id: int,
    include_nutrition: bool = True
) -> str
```

**Parameters:**
- `recipe_id` (int): The recipe ID from search results
- `include_nutrition` (bool): Whether to include nutrition information (default: True)

**Returns:**
- Formatted string with comprehensive recipe information including:
  - Basic info (servings, cooking time, scores)
  - Dietary tags and classifications
  - Complete ingredient list with measurements
  - Step-by-step instructions
  - Nutritional information
  - Wine pairing suggestions
  - Source information

**Examples:**

```python
# Basic recipe information
details = await get_recipe_details(recipe_id=1096211)

# With nutrition information
details = await get_recipe_details(
    recipe_id=1096211,
    include_nutrition=True
)
```

## Synchronous Versions

For use in non-async contexts, synchronous versions are available:

```python
from mcps.spoonacular_agent_tools import search_recipes_sync, get_recipe_details_sync

# Sync search
results = search_recipes_sync(query="pasta", cuisine="italian")

# Sync recipe details
details = get_recipe_details_sync(recipe_id=1096211)
```

## Agent Integration

### Example Agent Class

```python
import re
from mcps.spoonacular_agent_tools import search_recipes, get_recipe_details

class RecipeAgent:
    async def process_request(self, user_input: str) -> str:
        """Process user's recipe request"""
        
        # Check if user wants recipe details
        recipe_id_match = re.search(r'recipe (?:id )?(\d+)', user_input.lower())
        if recipe_id_match:
            recipe_id = int(recipe_id_match.group(1))
            return await get_recipe_details(recipe_id)
        
        # Extract search parameters
        query = self._extract_food_query(user_input)
        cuisine = self._extract_cuisine(user_input)
        diet = self._extract_diet(user_input)
        max_time = self._extract_time_constraint(user_input)
        
        # Search for recipes
        return await search_recipes(
            query=query,
            cuisine=cuisine,
            diet=diet,
            max_ready_time=max_time
        )
```

### Natural Language Processing

The tools are designed to work with natural language input. Here are some example patterns:

**Recipe Search Patterns:**
- "Find Italian pasta recipes"
- "Quick vegetarian dinner under 30 minutes"
- "Healthy chicken recipes with tomatoes but no dairy"
- "Easy gluten-free desserts"

**Recipe Detail Patterns:**
- "Recipe ID 1096211"
- "Get details for recipe 654005"
- "Show me recipe 650119"

## Output Format

### Search Results Format

```
🍽️ Found X recipes for 'query':

1. **Recipe Title** (ID: 123456)
   ⏱️ 30 min | 👥 4 servings | 🏥 Health: 85/100 | 💰 $2.50/serving
   🥬 Vegetarian | 🌾 Gluten-Free
   🌍 Cuisine: Italian, Mediterranean
   🍽️ Type: main course, dinner

2. **Another Recipe** (ID: 789012)
   ...
```

### Recipe Details Format

```
📋 **Recipe Title**

👥 **Servings:** 4
⏱️ **Ready in:** 30 minutes
🏥 **Health Score:** 85/100
💰 **Price per serving:** $2.50

🏷️ **Diet Tags:** 🥬 Vegetarian | 🌾 Gluten-Free

🌍 **Cuisines:** Italian, Mediterranean
🍽️ **Dish Types:** main course, dinner

🛒 **Ingredients:**
  • 1 lb pasta
  • 2 cloves garlic
  • 1/4 cup olive oil
  ...

👨‍🍳 **Instructions:**
  1. Bring a large pot of water to boil...
  2. Heat olive oil in a large pan...
  ...

📊 **Nutrition (per serving):**
  • **Calories:** 450.0kcal
  • **Fat:** 12.0g
  • **Carbohydrates:** 65.0g
  • **Protein:** 15.0g
  ...
```

## Error Handling

The tools include comprehensive error handling:

```python
# Missing API key
"❌ Error: SPOONACULAR_API_KEY environment variable not set"

# No results found
"🔍 No recipes found for: unusual query"

# API errors
"❌ Error searching recipes: API rate limit exceeded"

# Invalid recipe ID
"❌ Sorry, I couldn't retrieve details for recipe 999999: Recipe not found"
```

## Supported Cuisines

- Italian, Mexican, Indian, Chinese, Thai, Japanese
- French, Mediterranean, American, Korean, Spanish
- And many more...

## Supported Diets

- Vegetarian, Vegan
- Gluten Free, Dairy Free
- Keto, Paleo, Whole30
- And others...

## Testing

Run the test suite to verify functionality:

```bash
# Test async tools
python mcps/test_spoonacular_tools.py

# Test sync tools
python mcps/test_spoonacular_tools.py sync
```

## Interactive Demo

Try the interactive agent demo:

```bash
python mcps/agent_example.py
```

This will start an interactive session where you can type natural language recipe requests and see how the agent processes them.

## Dependencies

- httpx (for HTTP requests)
- pydantic (for data validation)
- Our modular Spoonacular client (in `utils/spoonacular/`)

## Rate Limiting

The tools respect Spoonacular's rate limits through the underlying modular client:
- Built-in retry logic with exponential backoff
- Rate limiting between requests
- Comprehensive error handling for API limits

## Best Practices

1. **Cache results** when possible to avoid repeated API calls
2. **Handle errors gracefully** and provide helpful fallback responses
3. **Use appropriate number limits** (5-10 recipes) for better user experience
4. **Extract recipe IDs** from search results for detailed information requests
5. **Validate user input** to ensure meaningful search queries

## Contributing

To add new features or improve the tools:

1. Extend the `SpoonacularTools` class in `spoonacular_mcp.py`
2. Add corresponding wrapper functions in `spoonacular_agent_tools.py`
3. Update tests in `test_spoonacular_tools.py`
4. Update this documentation

## License

This project uses the same license as the main project.