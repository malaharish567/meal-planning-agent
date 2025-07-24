import chromadb
from chromadb.config import Settings as ChromaSettings
import json
import os
from typing import List, Dict

class VectorDB:
    def __init__(self, persist_directory="./database/chroma_data"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        try:
            self.collection = self.chroma_client.get_collection("recipes")
        except:
            self.collection = self.chroma_client.create_collection("recipes")
    
    def add_recipes(self, recipes: List[Dict]):
        """Add recipes to vector database"""
        documents = []
        metadatas = []
        ids = []
        
        for recipe in recipes:
            # Create searchable text from ingredients and title
            ingredients_text = ', '.join([ing.get('name', '') for ing in recipe.get('usedIngredients', [])])
            ingredients_text += ', ' + ', '.join([ing.get('name', '') for ing in recipe.get('missedIngredients', [])])
            
            document = f"{recipe.get('title', '')} - Ingredients: {ingredients_text}"
            
            documents.append(document)
            metadatas.append({
                'title': recipe.get('title', ''),
                'id': str(recipe.get('id', '')),
                'image': recipe.get('image', ''),
                'used_ingredients': len(recipe.get('usedIngredients', [])),
                'missed_ingredients': len(recipe.get('missedIngredients', []))
            })
            ids.append(str(recipe.get('id', len(documents))))
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search_similar_recipes(self, query: str, n_results: int = 5):
        """Search for similar recipes based on query"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Error searching recipes: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}