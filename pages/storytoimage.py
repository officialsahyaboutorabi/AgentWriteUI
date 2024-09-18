import base64
from io import BytesIO
from IPython.display import HTML, display
from PIL import Image
import streamlit as st
import time
import os
import requests
import numpy as np
from dotenv import load_dotenv
from ollama import Client
import sys
from LLMs.llm import get_models
import openai
import os
import json
from base64 import b64decode
from openai import OpenAI
import logging
import httpx

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

klient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load environment variables
load_dotenv()

def get_available_models():
    """Fetch and return a list of available models from Ollama."""
    try:
        host_url = "http://localhost:11434/"
        client = Client(host=host_url)
        models = client.list()
        return [model['name'] for model in models['models']]
    except httpx.ConnectTimeout:
        st.warning("Unable to connect to Ollama server. Please ensure it's running.")
        return "Ollama server not available"
    except Exception as e:
        st.error(f"An error occurred while fetching models: {str(e)}")
        return "Error fetching models"

available_models = get_available_models()

# Define available LLM options
llm_options = ["GROQ", "OpenAI", "Ollama"]


def generate_image(prompt, llm_name, model_name, imagefilename):
    start_time = time.time()  # Start timing here

    try:
        logger.info(f"Starting image generation with LLM: {llm_name}, Model: {model_name}")

        if llm_name == "OpenAI":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.error("OPENAI_API_KEY environment variable not set")
                raise RuntimeError("OPENAI_API_KEY environment variable not set")
            logger.info(f"Using OpenAI model {model_name}")
            
            # OpenAI API call
            response = klient.images.generate(
                model=model_name,
                prompt=prompt,
                size="1024x1024",
                n=1,
                response_format="url",
            )

            # print response
            print(response)
            # save the image
            image_dir = "./generatedimages/"
            generated_image_name = f"{imagefilename}.png"  # any name you like; the filetype should be .png
            generated_image_filepath = os.path.join(image_dir, generated_image_name)
            generated_image_url = response.data[0].url  # extract image URL from response
            generated_image = requests.get(generated_image_url).content  # download the image

            with open(generated_image_filepath, "wb") as image_file:
                image_file.write(generated_image)  # write the image to the file

        elif llm_name == "Ollama":
            logger.error(f"Unsupported LLM: {llm_name}")
            return None, "You can only use OpenAI for Story-To-Image Generation!"

        else:
            logger.error(f"Unknown LLM selected: {llm_name}")
            return None, "Unknown LLM selected"

        duration = time.time() - start_time
        return generated_image, f"Time taken: {duration:.2f} seconds"

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Error during image generation: {e}")
        return None, f"Image generation failed."

    
def main():
    # Streamlit app layout
    st.title("Image Generation from Story")

    # Input form for user prompt and model selection
    with st.form(key="prompt_form"):
        imagefilename = st.text_area("Enter the name of your image (do not include the filetype):", "maninmoon")
        prompt = st.text_area("Enter your story to generate an image:", "Generate an image based on a story I wrote: A man walked across the moon.")
        llm_provider = st.sidebar.selectbox("Select LLM Provider", llm_options, index=0)
    
        if llm_provider == "OpenAI":
            llm_model = st.sidebar.selectbox("Select LLM Model", options=get_models(llm_provider), index=0)
        else:
            st.warning("You can only use OpenAI for Story-To-Image Generation!")

        model = llm_model
        #num_ctx = st.number_input("Enter the context size (num_ctx):", min_value=1024, max_value=8192, value=4096)
    
        # Submit button
        submit_button = st.form_submit_button(label="Generate Image")

    # If the form is submitted, generate the image
    if submit_button:
        logger.info(f"Generate button pressed with provider: {llm_provider} and model: {llm_model}")
        generated_image, duration = generate_image(prompt, llm_provider, llm_model, imagefilename)

        st.subheader("Generated Image")
        if generated_image:
            st.image(generated_image, caption="Generated Image", use_column_width=True)
        st.write(duration)

        st.session_state.last_inputs = {
            'llm_provider': llm_provider,
            'llm_model': llm_model
        }
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
            llm_provider = st.sidebar.selectbox("Select LLM Provider", llm_options, index=provider_index)
        
            # Update the model dropdown based on the selected provider
            if llm_provider == "Ollama":
                models = get_available_models()
            else:
                models = get_models(llm_provider)
        
            model_index = models.index(selected_model_name) if selected_model_name in models else 0
            llm_model = st.sidebar.selectbox("Select LLM Model", options=models, index=model_index)
            
            # Ensure the selected values are updated in the session state
            st.session_state.last_inputs['llm_provider'] = llm_provider
            st.session_state.last_inputs['llm_model'] = llm_model

        update_selection()
    
if __name__ == "__main__":
    main()
