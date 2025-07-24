from langchain.tools import Tool
from services.recipe_service import RecipeService
from database.vector_db import VectorDB
from utils.ingreadient_parser import IngredientParser

class AgentTools:
    def __init__(self):
        self.recipe_service = RecipeService()
        self.vector_db = VectorDB()
        self.ingredient_parser = IngredientParser()
        self.current_recipes = []  # Store current search results
    
    def search_recipes_tool(self, ingredients_input: str) -> str:
        """Tool to search recipes based on available ingredients"""
        # Parse ingredients
        ingredients = self.ingredient_parser.parse_ingredients(ingredients_input)
        
        if not ingredients:
            return "I couldn't identify any ingredients. Please list your available ingredients clearly."
        
        # Search recipes using Spoonacular API
        recipes = self.recipe_service.search_recipes_by_ingredients(ingredients, number=5)
        
        if not recipes:
            return f"I couldn't find recipes with ingredients: {', '.join(ingredients)}. Try different ingredients."
        
        # Store recipes for potential detailed lookup
        self.current_recipes = recipes
        
        # Format results with more detail
        result = f"Great! I found some delicious recipes using: **{', '.join(ingredients)}**\n\n"
        
        for i, recipe in enumerate(recipes[:3], 1):
            title = recipe.get('title', 'Unknown Recipe')
            recipe_id = recipe.get('id')
            used_ingredients = recipe.get('usedIngredients', [])
            missed_ingredients = recipe.get('missedIngredients', [])
            
            result += f"## {i}. {title}\n"
            result += f"🟢 **Uses your ingredients:** {', '.join([ing['name'] for ing in used_ingredients])}\n"
            
            if missed_ingredients:
                result += f"🔸 **You'll also need:** {', '.join([ing['name'] for ing in missed_ingredients])}\n"
            
            result += f"📋 **Recipe ID:** {recipe_id} (mention this for detailed instructions)\n\n"
        
        result += "🍳 **Want the full recipe?** Just ask me: 'Give me detailed instructions for recipe [ID]' or 'How do I make [recipe name]?'\n"
        result += f"💡 **My recommendation:** Try recipe {recipes[0].get('id')} - **{recipes[0].get('title')}** as it uses most of your ingredients!"
        
        return result
    
    def get_recipe_details_tool(self, recipe_id_or_name: str) -> str:
        """Tool to get detailed recipe instructions"""
        # If it's a recipe ID (numeric), fetch details directly
        if recipe_id_or_name.isdigit():
            recipe_details = self.recipe_service.get_recipe_details(int(recipe_id_or_name))
        else:
            # If it's a recipe name, we'll provide a general cooking method
            return self._provide_general_cooking_method(recipe_id_or_name)
        
        if not recipe_details:
            return f"I couldn't find detailed instructions for that recipe. Let me provide some general cooking guidance instead."
        
        # Format the detailed recipe
        result = f"## {recipe_details.get('title', 'Recipe')}\n\n"
        
        # Cooking time and servings
        ready_in_minutes = recipe_details.get('readyInMinutes', 'N/A')
        servings = recipe_details.get('servings', 'N/A')
        result += f"⏱️ **Prep Time:** {ready_in_minutes} minutes | 👥 **Serves:** {servings}\n\n"
        
        # Ingredients
        result += "### 📝 Ingredients:\n"
        ingredients = recipe_details.get('extendedIngredients', [])
        for ingredient in ingredients:
            amount = ingredient.get('amount', '')
            unit = ingredient.get('unit', '')
            name = ingredient.get('name', '')
            result += f"- {amount} {unit} {name}\n"
        
        result += "\n### 🍳 Instructions:\n"
        
        # Instructions
        instructions = recipe_details.get('analyzedInstructions', [])
        if instructions and len(instructions) > 0:
            steps = instructions[0].get('steps', [])
            for i, step in enumerate(steps, 1):
                step_text = step.get('step', '')
                result += f"{i}. {step_text}\n\n"
        else:
            # Fallback if no detailed instructions
            result += "Detailed step-by-step instructions are not available for this recipe. Here's what I can tell you:\n"
            result += f"This recipe takes about {ready_in_minutes} minutes to prepare and serves {servings} people.\n"
            result += "Follow standard cooking methods for the main ingredients listed above.\n"
        
        # Additional tips
        if recipe_details.get('summary'):
            summary = recipe_details.get('summary', '').replace('<b>', '**').replace('</b>', '**')
            # Remove HTML tags
            import re
            summary = re.sub('<.*?>', '', summary)
            result += f"\n### 💡 Tips:\n{summary[:200]}...\n"
        
        return result
    
    def _provide_general_cooking_method(self, recipe_name: str) -> str:
        """Provide general cooking guidance when specific recipe details aren't available"""
        recipe_name_lower = recipe_name.lower()
        
        if 'strata' in recipe_name_lower:
            return """
## General Strata Cooking Method

### 📝 Basic Strata Ingredients:
- Bread (cubed, day-old preferred)
- Eggs (6-8 for a 9x13 pan)
- Milk or cream (2-3 cups)
- Cheese (1-2 cups, shredded)
- Your available ingredients (mushrooms, bacon, etc.)
- Salt, pepper, herbs

### 🍳 Instructions:
1. **Prep:** Preheat oven to 350°F (175°C). Grease a 9x13 baking dish.

2. **Layer:** Place cubed bread in the bottom of the dish.

3. **Add Fillings:** Layer your mushrooms, cooked bacon, and any other ingredients over the bread.

4. **Make Custard:** Whisk eggs with milk, salt, pepper, and herbs.

5. **Combine:** Pour egg mixture over bread and fillings. Press down gently.

6. **Rest:** Let sit for 15-30 minutes so bread absorbs liquid.

7. **Top:** Sprinkle cheese on top.

8. **Bake:** 45-60 minutes until center is set and top is golden.

9. **Cool:** Let rest 10 minutes before serving.

### 💡 Tips:
- Can be assembled the night before and baked in the morning
- Test doneness by inserting a knife in center - should come out clean
            """
        
        return f"I can provide general cooking guidance for {recipe_name}, but I'd need the specific recipe ID to get detailed instructions. Would you like me to search for more specific recipes instead?"
    
    def get_tools(self):
        """Return list of tools for the agent"""
        return [
            Tool(
                name="search_recipes",
                description="Search for recipes based on available ingredients. Input should be a list of ingredients.",
                func=self.search_recipes_tool
            ),
            Tool(
                name="get_recipe_details",
                description="Get detailed cooking instructions for a specific recipe.",
                func=self.get_recipe_details_tool
            )
        ]