import streamlit as st
import time
import base64
import logging
import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from tools import write_markdown_file
from openai import OpenAI
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnableLambda
from operator import itemgetter
from ollama import Client
import sys

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

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ollama_client = Client(host="http://localhost:11434")

# Define available LLM options
llm_options = ["Ollama"]

# Function to fetch models from Ollama
def get_available_models():
    """Fetch and return a list of available models from Ollama."""
    try:
        client = Client(host="http://localhost:11434/")
        models = client.list()
        return [model['name'] for model in models['models']]
    except Exception as e:
        st.error(f"Error fetching models: {str(e)}")
        return ["Ollama server not available"]

# Function to fetch the list of models
def fetch_models():
    host_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:11434/"
    fetchmodelclient = Client(host=host_url)
    model_list = fetchmodelclient.list()
    return [model['model'] for model in model_list['models']]

# Fetch models initially
model_names = fetch_models()

def main():

    st.title("🖼️ Image to Story Generator")

    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None

    # Sidebar settings
    st.sidebar.title("Settings")
    llm_provider = st.sidebar.selectbox("Select LLM Provider", llm_options, index=0)
    
    if llm_provider == "Ollama":
        # Dynamic model selection via dropdown
        models = get_available_models()
        llm_model = st.sidebar.selectbox("Select LLM Model", models)
    if llm_provider == "Ollama":
        if isinstance(llm_model, str):
            llm = Ollama(model=llm_model)
        else:
            st.error("Invalid model selection for Ollama.")
            return
    else:
        # Placeholder for other models (e.g., GROQ, OpenAI) Unfortunately only Ollama can run both Image to Story and Text Story Writing.
        st.warning("Image to Story only works with Ollama currently. Sorry for the inconvenience.") #llm_model = st.sidebar.selectbox("Select LLM Model", options=get_models(llm_provider), index=0)

    # User inputs
    num_words = st.number_input("Maximum number of words for the story", min_value=50, max_value=1000, value=200)

    with st.sidebar.expander("Advanced Options"):
        num_steps = st.sidebar.slider("Number of Steps", min_value=0, max_value=4, value=0, step=1)

    # Image upload
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Initialize the selected LLM model
    llm = Ollama(model=llm_model)
    
    # Function to bind and run LLM with an image and prompt
    def bind_and_run_llm(image_base64, prompt_text):
        """Bind and run the LLM with the given image and prompt text."""
        bound = llm.bind(images=[image_base64])
        return bound.invoke(prompt_text)

    # Define the prompt template
    prompt_template = f"""
    You are the world's best fictional-genre book writer and storyteller;
    You have multiple book awards;
    You can generate a short story based on a simple narrative;
    The story must not be longer than {num_words} words;
    """

    # Create the prompt
    prompt = PromptTemplate.from_template(prompt_template)
    
    # Initialize response variable
    response = ""

    if uploaded_image is not None:
            # Convert the uploaded image to base64
            image = uploaded_image.getvalue()
            b64 = base64.b64encode(image).decode()
            
            st.image(image, caption="Uploaded Image", use_column_width=True)

    # Add a "Generate" button
    if st.button("Generate Story"):
        start_time = time.time()
        if uploaded_image is not None:

            # Generate the prompt text
            prompt_text = prompt.format(num_words=num_words)

            # Initialize progress bar
            progress_text = "Writing story from image..."
            progress_bar = st.progress(0, text=progress_text)

            try:
                # Simulate progress for demo purposes
                for percent_complete in range(100):
                    time.sleep(0.01)  # Simulate time-consuming task
                    progress_bar.progress(percent_complete + 1, text=progress_text)

                # Invoke the LLM with the selected model and inputs
                response = bind_and_run_llm(b64, prompt_text)

                # Finalize progress
                progress_bar.progress(100, text="Story generation complete!")
                time.sleep(1)  # Allow the final progress update to be visible
                progress_bar.empty()

                # Calculate duration and word count after receiving response
                end_time = time.time()
                duration = end_time - start_time
                
                # Count the number of words in the response
                word_count = len(response.split())

                logger.info("Story generation completed successfully")
                logger.debug(f"LLM Model: {llm_model}, Time taken: {duration:.2f} seconds, Word count: {word_count}")

                # Write response to markdown file
                write_markdown_file(response, "generated_image_to_story")
                logger.info(f"Output written to markdown file")

            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                logger.error(f"Error during workflow execution: {e}")
                st.error(f"Error during workflow execution: {e}")

            # Invoke the LLM with the selected model and inputs
            response = bind_and_run_llm(b64, prompt_text)
        else:
            st.warning("Please upload an image first")

    # Display the generated story if available
    if response:
        st.subheader("Generated Output")
        st.text_area("Output", response, height=300)
        st.write(f"Time taken: {duration:.2f} seconds")
        st.write(f"Word count: {word_count}")

if __name__ == "__main__":
    main()

