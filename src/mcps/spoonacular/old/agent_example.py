"""
Example agent integration showing how to use Spoonacular tools.

This demonstrates how an AI agent can use the Spoonacular tools to:
1. Search for recipes based on user preferences
2. Get detailed information about specific recipes
3. Handle dietary restrictions and preferences
4. Provide nutrition information
"""

import os
import sys
import asyncio
import re

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcps.spoonacular_agent_tools import search_recipes, get_recipe_details


class RecipeAgent:
    """
    Example AI agent that uses Spoonacular tools to help users find recipes.
    """
    
    def __init__(self):
        self.conversation_history = []
    
    async def process_user_request(self, user_input: str) -> str:
        """
        Process a user's recipe request and return helpful information.
        
        Args:
            user_input: Natural language request from user
            
        Returns:
            Formatted response with recipe information
        """
        user_input_lower = user_input.lower()
        
        # Extract information from user input
        dietary_preferences = self._extract_dietary_preferences(user_input_lower)
        cuisine_preference = self._extract_cuisine(user_input_lower)
        time_constraint = self._extract_time_constraint(user_input_lower)
        main_query = self._extract_main_query(user_input_lower)
        
        # If user is asking for recipe details by ID
        recipe_id_match = re.search(r'recipe (?:id )?(\d+)|id[:\s]*(\d+)', user_input_lower)
        if recipe_id_match:
            recipe_id = int(recipe_id_match.group(1) or recipe_id_match.group(2))
            return await self._get_recipe_details(recipe_id)
        
        # Otherwise, search for recipes
        return await self._search_recipes(
            query=main_query,
            cuisine=cuisine_preference,
            diet=dietary_preferences,
            max_time=time_constraint,
            user_input=user_input
        )
    
    def _extract_dietary_preferences(self, text: str) -> str:
        """Extract dietary preferences from user input"""
        diets = {
            'vegetarian': ['vegetarian', 'veggie'],
            'vegan': ['vegan'],
            'gluten free': ['gluten free', 'gluten-free', 'celiac'],
            'dairy free': ['dairy free', 'dairy-free', 'lactose intolerant'],
            'keto': ['keto', 'ketogenic', 'low carb'],
            'paleo': ['paleo'],
            'whole30': ['whole30', 'whole 30']
        }
        
        for diet_name, keywords in diets.items():
            if any(keyword in text for keyword in keywords):
                return diet_name
        return None
    
    def _extract_cuisine(self, text: str) -> str:
        """Extract cuisine preference from user input"""
        cuisines = {
            'italian': ['italian', 'italy'],
            'mexican': ['mexican', 'mexico'],
            'indian': ['indian', 'india'],
            'chinese': ['chinese', 'china'],
            'thai': ['thai', 'thailand'],
            'japanese': ['japanese', 'japan', 'sushi'],
            'french': ['french', 'france'],
            'mediterranean': ['mediterranean', 'greek'],
            'american': ['american', 'usa'],
            'korean': ['korean', 'korea'],
            'spanish': ['spanish', 'spain']
        }
        
        for cuisine_name, keywords in cuisines.items():
            if any(keyword in text for keyword in keywords):
                return cuisine_name
        return None
    
    def _extract_time_constraint(self, text: str) -> int:
        """Extract time constraint from user input"""
        # Look for patterns like "30 minutes", "under 45 min", "quick", etc.
        time_patterns = [
            r'(?:under|less than|within|in)\s*(\d+)\s*(?:min|minute)',
            r'(\d+)\s*(?:min|minute)(?:s)?\s*(?:or less|max|maximum)',
            r'quick(?:ly)?\s*(?:\((\d+)\s*(?:min|minute))?',
            r'fast(?:\s*\((\d+)\s*(?:min|minute))?'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match and match.group(1):
                return int(match.group(1))
        
        # Default time constraints for keywords
        if 'quick' in text or 'fast' in text:
            return 20
        if 'easy' in text:
            return 30
        
        return None
    
    def _extract_main_query(self, text: str) -> str:
        """Extract the main food/dish query from user input"""
        # Remove common phrases to get to the core query
        cleanup_phrases = [
            r'i want to (?:cook|make|prepare)\s*',
            r'i\'m looking for\s*',
            r'can you find\s*',
            r'show me\s*',
            r'search for\s*',
            r'find me\s*',
            r'recipe for\s*',
            r'how to make\s*'
        ]
        
        cleaned_text = text
        for phrase in cleanup_phrases:
            cleaned_text = re.sub(phrase, '', cleaned_text)
        
        # Extract food-related words (simplified approach)
        food_words = []
        words = cleaned_text.split()
        
        # Skip common non-food words
        skip_words = {
            'i', 'want', 'to', 'cook', 'make', 'with', 'without', 'and', 'or',
            'that', 'is', 'are', 'can', 'will', 'would', 'should', 'could',
            'quick', 'easy', 'fast', 'healthy', 'delicious', 'tasty', 'good',
            'vegetarian', 'vegan', 'gluten', 'free', 'dairy', 'keto', 'paleo',
            'italian', 'mexican', 'indian', 'chinese', 'thai', 'japanese',
            'under', 'less', 'than', 'within', 'minutes', 'mins', 'min'
        }
        
        for word in words:
            word_clean = re.sub(r'[^\w]', '', word).lower()
            if word_clean and word_clean not in skip_words and len(word_clean) > 2:
                food_words.append(word_clean)
        
        return ' '.join(food_words[:3])  # Take first 3 relevant words
    
    async def _search_recipes(
        self,
        query: str,
        cuisine: str = None,
        diet: str = None,
        max_time: int = None,
        user_input: str = ""
    ) -> str:
        """Search for recipes and format the response"""
        
        if not query:
            query = "dinner"  # Default fallback
        
        response = [f"🍽️ **Recipe Search Results**"]
        response.append(f"Looking for: {query}")
        
        if cuisine:
            response.append(f"Cuisine: {cuisine.title()}")
        if diet:
            response.append(f"Diet: {diet.title()}")
        if max_time:
            response.append(f"Max cooking time: {max_time} minutes")
        
        response.append("")
        
        try:
            # Perform the search
            search_result = await search_recipes(
                query=query,
                cuisine=cuisine,
                diet=diet,
                max_ready_time=max_time,
                number=5
            )
            
            response.append(search_result)
            
            # Add helpful suggestions
            response.append("💡 **Tips:**")
            response.append("• Say 'recipe ID [number]' to get detailed instructions")
            response.append("• Ask for specific cuisines like 'Italian pasta' or 'Thai curry'")
            response.append("• Mention dietary needs like 'vegetarian' or 'gluten free'")
            response.append("• Specify time constraints like 'quick dinner under 30 minutes'")
            
        except Exception as e:
            response.append(f"❌ Sorry, I encountered an error: {str(e)}")
            response.append("Please try again with a different search term.")
        
        return "\n".join(response)
    
    async def _get_recipe_details(self, recipe_id: int) -> str:
        """Get detailed recipe information"""
        try:
            details = await get_recipe_details(recipe_id, include_nutrition=True)
            
            response = [f"📋 **Detailed Recipe Information**"]
            response.append("")
            response.append(details)
            response.append("")
            response.append("💡 **Need something else?**")
            response.append("• Search for more recipes with terms like 'find chicken recipes'")
            response.append("• Ask for specific dietary needs or cuisines")
            response.append("• Request cooking time constraints")
            
            return "\n".join(response)
            
        except Exception as e:
            return f"❌ Sorry, I couldn't retrieve details for recipe {recipe_id}: {str(e)}"


async def demo_conversation():
    """Demonstrate a conversation with the recipe agent"""
    
    agent = RecipeAgent()
    
    print("🤖 Recipe Agent Demo")
    print("=" * 50)
    
    # Simulate various user requests
    test_requests = [
        "I want to make pasta for dinner",
        "Find me a quick vegetarian Indian curry under 30 minutes",
        "Show me healthy gluten-free chicken recipes",
        "Recipe ID 1096211",  # Get details for a specific recipe
        "I'm looking for easy Italian dishes with tomatoes but no cheese"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"👤 **User:** {request}")
        print()
        
        response = await agent.process_user_request(request)
        print(f"🤖 **Agent:**")
        print(response)
        print()
        print("-" * 50)
        print()


async def interactive_demo():
    """Interactive demo where user can type requests"""
    
    agent = RecipeAgent()
    
    print("🤖 Interactive Recipe Agent")
    print("=" * 50)
    print("Ask me to find recipes! Examples:")
    print("• 'Find Italian pasta recipes'")
    print("• 'Quick vegetarian dinner under 30 minutes'")
    print("• 'Recipe ID 1096211' for detailed info")
    print("• Type 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🤖 Goodbye! Happy cooking! 👨‍🍳")
                break
            
            if not user_input:
                continue
            
            print("🤖 Agent: (searching...)")
            response = await agent.process_user_request(user_input)
            print(f"🤖 Agent:\n{response}")
            print()
            
        except KeyboardInterrupt:
            print("\n🤖 Goodbye! Happy cooking! 👨‍🍳")
            break
        except Exception as e:
            print(f"🤖 Sorry, I encountered an error: {e}")


if __name__ == "__main__":
    # Check if API key is available
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        print("❌ Please set SPOONACULAR_API_KEY environment variable to run the demo")
        exit(1)
    
    print("Choose demo mode:")
    print("1. Automated demo with sample requests")
    print("2. Interactive mode (type your own requests)")
    
    try:
        choice = input("Enter 1 or 2: ").strip()
        
        if choice == "1":
            asyncio.run(demo_conversation())
        elif choice == "2":
            asyncio.run(interactive_demo())
        else:
            print("Running automated demo...")
            asyncio.run(demo_conversation())
            
    except KeyboardInterrupt:
        print("\nDemo interrupted. Goodbye!")