from langchain_groq import ChatGroq
from config.settings import settings

class GroqService:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.7,
            groq_api_key=settings.GROQ_API_KEY,
            model_name="llama3-70b-8192"
        )
    
    def get_llm(self):
        return self.llm
