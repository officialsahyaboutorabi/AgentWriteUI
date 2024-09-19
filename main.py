import streamlit as st
import time
import httpx
from LLMs.llm import get_models
from dotenv import load_dotenv
from tools import write_markdown_file
from ollama import Client
from graph import create_workflow
import logging
import os
import sys
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import json

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

# Ensure the path is correct
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Function to load translations
def load_translations():
    with open("translation/lang.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Load translations
translations = load_translations()

# Function to get the translated text based on the current language
def get_translation(key):
    if 'selected_language' not in st.session_state:
        st.session_state['selected_language'] = 'en'  # Default to English if not set
    lang = st.session_state['selected_language']
    return translations.get(lang, {}).get(key, key)

# Define available languages with translatable names
languages = {
    get_translation("English"): "en",
    get_translation("German"): "de",
    get_translation("Japanese"): "ja",
    get_translation("Turkish"): "tr",
    get_translation("Farsi"): "ir",
    get_translation("Dutch"): "nl",
    get_translation("Italian"): "it",
    get_translation("Russian"): "ru",
    get_translation("Chinese"): "zh"
}
# Initialize default language if not set
if 'selected_language' not in st.session_state:
    st.session_state['selected_language'] = list(languages.values())[0]

# Define the translation function BEFORE usage
def _(key):
    return translations.get(st.session_state['selected_language'], {}).get(key, key)


def get_available_models():
    """Fetch and return a list of available models from Ollama."""
    try:
        host_url = "http://localhost:11434/"
        client = Client(host=host_url)
        models = client.list()
        return [model['name'] for model in models['models']]
    except httpx.ConnectTimeout:
        st.warning(_("Unable to connect to Ollama server. Please ensure it's running."))
        return [_("Ollama server not available")]
    except Exception as e:
        st.error(f"{_('An error occurred while fetching models')}: {str(e)}")
        return [_("Error fetching models")]

available_models = get_available_models()

# Define available LLM options
llm_options = ["GROQ", "OpenAI", "Ollama"]

from langchain_groq import ChatGroq
from ollama import Client
from openai import OpenAI

olclient = Client(host='http://localhost:11434')
klient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_writing(instruction, num_steps, llm_name, model_name, storytitle):
    start_time = time.time()  # Start timing here

    try:
        logger.info(f"Starting writing generation with LLM: {llm_name}, Model: {model_name}")

        if llm_name == "OpenAI":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.error(_("OPENAI_API_KEY environment variable not set"))
                raise RuntimeError(_("OPENAI_API_KEY environment variable not set"))
            logger.info(f"Using OpenAI model {model_name}")
            write_path = os.path.join(os.path.dirname(__file__), 'chains/prompts', 'write.txt')
            with open(write_path, 'r') as file:
                write_path = file.read()

            # OpenAI API call
            response = klient.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": write_path},
                    {"role": "user", "content": instruction},
                ],
                stream=True
            )

            final_doc = ""
            word_count = 0
            for chunk in response:
                if hasattr(chunk, 'choices') and chunk.choices:
                    choice = chunk.choices[0]
                    delta = choice.delta
                    if delta and delta.content:
                        content = delta.content
                        final_doc += content
                        word_count += len(content.split())
                else:
                    logger.warning(f"Unexpected chunk format: {chunk}")

        elif llm_name == "GROQ":
            logger.info(f"Using GROQ model {model_name}")

            # Ensure you use the GROQ-specific API or client
            LLM = ChatGroq(model=model_name, temperature=0)
            app = create_workflow(LLM)
    
            # Inputs for the GROQ model workflow
            inputs = {
                "initial_prompt": instruction,
                "num_steps": num_steps,
                "llm_name": llm_name,
                "model_name": model_name,
                "storytitle": storytitle
            }
    
            # Invoke the workflow and get the result
            output = app.invoke(inputs)

            # Handle the output from the GROQ model
            final_doc = output.get('final_doc', _('No output generated.'))
            word_count = output.get('word_count', 0)
            
        elif llm_name == "Ollama":
            logger.info(f"Using Ollama model {model_name}")
            write_path = os.path.join(os.path.dirname(__file__), 'chains/prompts', 'write.txt')
            with open(write_path, 'r') as file:
                write_content = file.read()

            # Ollama API call
            response = olclient.chat(
                model=model_name, 
                messages=[
                    {"role": "system", "content": write_content},
                    {"role": "user", "content": instruction},
                ],
                stream=True
            )
            final_doc = ""
            word_count = 0

            for chunk in response:
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    final_doc += content
                    word_count += len(content.split())
                else:
                    logger.warning(f"Unexpected chunk format: {chunk}")

        else:
            logger.error(f"{_('Unknown LLM selected')}: {llm_name}")
            return _("Unknown LLM selected"), "", 0

        duration = time.time() - start_time
        logger.info(_("Workflow created successfully"))
        logger.debug(f"llm_name: {llm_name}, model_name: {model_name}")

        write_markdown_file(final_doc, f"{model_name}-{storytitle}")
        logger.info(_("Output written to markdown file"))

        return final_doc, f"{_('Time taken')}: {duration:.2f} {_('seconds')}", word_count

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"{_('Error during workflow execution')}: {e}")
        st.error(f"{_('Error during workflow execution')}: {e}")
        return _("An error occurred while generating the writing."), "", 0

# Language selection dropdown
def update_language(selected_language_key):
    selected_language_value = languages[selected_language_key]
    st.session_state['selected_language'] = selected_language_value

def main():
    # Language selection dropdown
    selected_language_key = st.sidebar.selectbox(
        _("Select Language"), 
        options=list(languages.keys()), 
        index=list(languages.values()).index(st.session_state['selected_language'])
    )

    if languages[selected_language_key] != st.session_state['selected_language']:
        update_language(selected_language_key)

    st.title(_("📝 AgentWriting UI"))
    st.subheader(_("An AI Writing Assistant"))

    # User inputs
    storytitle = st.text_area(_("Title of the Story"), _("Give a name to your story."))
    instruction = st.text_area(_("Enter Writing Instruction"), _("Type the writing prompt or instruction here."))
    
    # Sidebar for settings
    st.sidebar.title(_("Settings"))

    with st.sidebar.expander(_("Advanced Options")):
        num_steps = st.slider(_("Number of Steps"), min_value=0, max_value=4, value=0, step=1)

    llm_provider = st.sidebar.selectbox(_("Select LLM Provider"), llm_options, index=0)
    
    if llm_provider == "Ollama":
        llm_model = st.sidebar.selectbox(_("Select LLM Model"), options=get_available_models(), index=0)
    else:
        llm_model = st.sidebar.selectbox(_("Select LLM Model"), options=get_models(llm_provider), index=0)

    # Generate button
    if st.button(_("Generate")):
        logger.info(f"Generate button pressed with provider: {llm_provider} and model: {llm_model}")
        output, duration, word_count = generate_writing(instruction, num_steps, llm_provider, llm_model, storytitle)
        st.subheader(_("Generated Output"))
        st.text_area(_("Output"), output, height=300)  # Pass height directly, no translation needed
        st.write(_(duration))
        st.write(_(f"Word Count: {word_count}"))

        st.session_state.last_inputs = {
            'instruction': instruction,
            'num_steps': num_steps,
            'llm_provider': llm_provider,
            'llm_model': llm_model,
            'storytitle': storytitle
        }

    # Regenerate button
    if st.button(_("Regenerate")):
        if 'last_inputs' in st.session_state:
            last_inputs = st.session_state.last_inputs
            output, duration, word_count = generate_writing(
                last_inputs['instruction'],
                last_inputs['num_steps'],
                last_inputs['llm_provider'],
                last_inputs['llm_model'],
                last_inputs['storytitle']
            )
            st.subheader(_("Generated Output"))
            st.text_area(_("Output"), output, height=300)  # Pass height directly, no translation needed
            st.write(_(f"Time taken: {duration}"))
            st.write(_(f"Word Count: {word_count}"))
        else:
            st.warning(_("No previous input available for regeneration."))

    def update_selection():
        if 'last_inputs' in st.session_state:
            # Lambda functions to get selected values
            get_selected_provider = lambda: st.session_state.last_inputs.get('llm_provider')
            get_selected_model_name = lambda: st.session_state.last_inputs.get('llm_model')
        
            # Retrieve the selected values
            selected_provider = get_selected_provider()
            selected_model_name = get_selected_model_name()
        
            # Update the provider dropdown
            provider_index = llm_options.index(selected_provider) if selected_provider in llm_options else 0
            llm_provider = st.sidebar.selectbox(_("Select LLM Provider"), llm_options, index=provider_index)
        
            # Update the model dropdown based on the selected provider
            if llm_provider == "Ollama":
                models = get_available_models()
            else:
                models = get_models(llm_provider)
        
            model_index = models.index(selected_model_name) if selected_model_name in models else 0
            llm_model = st.sidebar.selectbox(_("Select LLM Model"), options=models, index=model_index)
            
            # Ensure the selected values are updated in the session state
            st.session_state.last_inputs['llm_provider'] = llm_provider
            st.session_state.last_inputs['llm_model'] = llm_model

        update_selection()
    
if __name__ == "__main__":
    main()
