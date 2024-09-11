import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
#from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_fireworks import ChatFireworks
from langchain_ollama import ChatOllama
from ollama import Client

# Load environment variables from .env file
load_dotenv()

# Define function to fetch models from Ollama
def get_ollama_models():
    host_url = "http://localhost:11434/"
    client = Client(host=host_url)
    model_list = client.list()
    return [model['model'] for model in model_list['models']]


def get_models(provider):
    """
    Returns a list of model names based on the selected LLM provider.
    """
    if provider == "GROQ":
        return ["llama-3.1-70b-versatile", "gemma-7b-it"]  # Example model names
    elif provider == "OpenAI":
        return ["gpt-3.5-turbo", "gpt-4o"]  # Example model names
    #elif provider == "Google":
        #return ["gemini-1.5-flash-exp-0827", "other-google-model"]  # Example model names
    elif provider == "Ollama":
        return get_ollama_models()  # Example model names
    else:
        return []


# Initialize LLM
LLM = ChatGroq(model="llama-3.1-70b-versatile", temperature=0)

OPENAI_LLM = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))


# LLM = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash-exp-0827",
#     temperature=0,
#     )


# FIREWORKS_LLM = ChatFireworks(model="accounts/fireworks/models/llama-v3-70b-instruct")

OLLAMA_LLM = ChatOllama(model="llama3.1", temperature=0) # format="json")
