import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_models(provider):
    """
    Returns a list of model names based on the selected LLM provider.
    """
    if provider == "GROQ":
        return ["llama-3.1-70b-versatile", "gemma-7b-it"]  # Example model names
    elif provider == "OpenAI":
        return ['gpt-3.5-turbo', 'gpt-4']  # Example model names
    
    else:
        return []
