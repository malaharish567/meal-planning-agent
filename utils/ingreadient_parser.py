import re
from typing import List

class IngredientParser:
    def __init__(self):
        # Common cooking terms to filter out
        self.cooking_terms = {'cup', 'cups', 'tablespoon', 'tablespoons', 'teaspoon', 'teaspoons', 
                             'pound', 'pounds', 'ounce', 'ounces', 'gram', 'grams', 'kg', 'lb',
                             'tbsp', 'tsp', 'oz', 'ml', 'liter', 'liters', 'fresh', 'dried',
                             'chopped', 'sliced', 'diced', 'minced', 'whole', 'ground'}
    
    def parse_ingredients(self, user_input: str) -> List[str]:
        """Parse user input to extract ingredient names"""
        # Convert to lowercase and split by common separators
        ingredients = re.split(r'[,\n\r]+', user_input.lower())
        
        cleaned_ingredients = []
        for ingredient in ingredients:
            # Remove extra whitespace
            ingredient = ingredient.strip()
            
            # Remove numbers and measurements
            ingredient = re.sub(r'\d+\.?\d*', '', ingredient)
            
            # Remove common measurement words
            words = ingredient.split()
            filtered_words = [word for word in words if word not in self.cooking_terms]
            
            if filtered_words:
                cleaned_ingredient = ' '.join(filtered_words).strip()
                if cleaned_ingredient and len(cleaned_ingredient) > 1:
                    cleaned_ingredients.append(cleaned_ingredient)
        
        return cleaned_ingredients