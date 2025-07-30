import requests
import json
from config.settings import settings

class RecipeService:
    def __init__(self):
        self.api_key = settings.SPOONACULAR_API_KEY
        self.base_url = settings.SPOONACULAR_BASE_URL
    
    def search_recipes_by_ingredients(self, ingredients, number=10):
        """Search recipes by available ingredients"""
        url = f"{self.base_url}/findByIngredients"
        params = {
            'apiKey': self.api_key,
            'ingredients': ','.join(ingredients),
            'number': number,
            'ranking': 1,
            'ignorePantry': True
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching recipes: {e}")
            return []
    
    def get_recipe_details(self, recipe_id):
        """Get detailed recipe information"""
        url = f"{self.base_url}/{recipe_id}/information"
        params = {
            'apiKey': self.api_key,
            'includeNutrition': True
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching recipe details: {e}")
            return None