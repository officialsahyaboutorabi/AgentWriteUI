# chains/pplan_chain.py
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import sys
import os
import logging

# Ensure the path is correct
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import functions from shared.py for model selection
from shared import get_selected_model_name, get_selected_provider

# Get the selected model name and provider
model_name = get_selected_model_name()
provider = get_selected_provider()

if not model_name or not provider:
    raise RuntimeError("Model or provider not selected or empty")

openaiurl = "https://api.openai.com/v1/completions"

# Dynamically import the LLM class based on the selected provider
if provider == "GROQ":
    from langchain_groq import ChatGroq
    LLM = ChatGroq(model=model_name, temperature=0)
elif provider == "OpenAI":
    from langchain_openai import ChatOpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    logger.info(f"Using OpenAI model {model_name}")
    LLM = ChatOpenAI(model=model_name, temperature=0, api_key=openai_api_key, base_url=openaiurl)
elif provider == "Ollama":
    from langchain_ollama import ChatOllama
    LLM = ChatOllama(model=model_name, temperature=0)
else:
    raise RuntimeError(f"Unsupported provider: {provider}")

# Load the plan prompt template
plan_template_path = os.path.join(os.path.dirname(__file__), 'prompts', 'plan.txt')
with open(plan_template_path, 'r') as file:
    plan_template = file.read()

# Create a ChatPromptTemplate
plan_prompt = ChatPromptTemplate([('user', plan_template)])

# Create the plan chain
plan_chain = plan_prompt | LLM | StrOutputParser()

# Note: You can now use `plan_chain` directly where needed in the script.

