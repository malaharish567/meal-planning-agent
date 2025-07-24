import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
    CHROMA_DB_PATH = "./database/chroma_data"
    SPOONACULAR_BASE_URL = "https://api.spoonacular.com/recipes"

settings = Settings()