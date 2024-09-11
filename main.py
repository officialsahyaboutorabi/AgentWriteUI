import gradio as gr
import sys
import os
import time
import httpx

# Ensure the correct path is set for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LLMs.llm import LLM, OLLAMA_LLM, OPENAI_LLM, get_models, get_ollama_models
from dotenv import load_dotenv
from graph import create_workflow
from tools import write_markdown_file
from ollama import Client

def get_available_models():
    """Fetch and return a list of available models from Ollama."""
    try:
        host_url = "http://localhost:11434/"
        client = Client(host=host_url)
        models = client.list()
        return [model['name'] for model in models['models']]
    except httpx.ConnectTimeout:
        print("Warning: Unable to connect to Ollama server. Please ensure it's running.")
        return ["Ollama server not available"]
    except Exception as e:
        print(f"An error occurred while fetching models: {str(e)}")
        return ["Error fetching models"]

available_models = get_available_models()


# Load environment variables
load_dotenv()

# Create the workflow using the LLM class
#app = create_workflow(LLM)

# Define available LLM options
llm_options = ["GROQ", "OpenAI", "Ollama"]  # Add other options as needed


def generate_writing(instruction, num_steps, llm_name, model_name):
    """
    Generates a piece of writing based on the user's input, selected LLM, and model.
    """
    try:
        # Dynamically select the LLM based on the user's choice
        if llm_name == "GROQ":
            app = create_workflow(LLM)  # Use the Groq model
        elif llm_name == "OpenAI":
            # Use the Ollama model if selected (make sure to define OPENAI_LLM properly)
            app = create_workflow(OPENAI_LLM)
        elif llm_name == "Ollama":
            # Use the Ollama model if selected (make sure to define OLLAMA_LLM properly)
            app = create_workflow(OLLAMA_LLM)
            pass  # Replace with the correct Ollama workflow logic
        else:
            return "Unknown LLM selected", ""

        inputs = {
            "initial_prompt": instruction,
            "num_steps": num_steps,
            "llm_name": llm_name,
            "model_name": model_name
        }
        
        start_time = time.time()  # Start timing
        
        output = app.invoke(inputs)
        duration = time.time() - start_time  # Calculate duration
        
        # Write the output to a markdown file
        write_markdown_file(output['final_doc'], "generated_writing")

        return output['final_doc'], f"Time taken: {duration:.2f} seconds", output['word_count']
    except Exception as e:
        print("Error during workflow execution:", e)  # Error handling
        return "An error occurred while generating the writing.", ""


# Gradio UI for AgentWriting
def gradio_app():
    last_inputs = {}  # Dictionary to store the last inputs
    # Function to generate writing using the selected LLM
    def on_generate_writing(instruction, num_steps, llm_provider, llm_model):
        # Store the inputs for reuse in regeneration
        last_inputs['instruction'] = instruction
        last_inputs['num_steps'] = num_steps
        last_inputs['llm_provider'] = llm_provider
        last_inputs['llm_model'] = llm_model

        return generate_writing(instruction, num_steps, llm_provider, llm_model)

    # Function to regenerate the writing using the last stored inputs
    def on_regenerate_writing():
        if not last_inputs:
            return "No previous input available for regeneration.", ""
        
        # Use the last stored inputs to regenerate the writing
        return generate_writing(
            last_inputs['instruction'],
            last_inputs['num_steps'],
            last_inputs['llm_provider'],
            last_inputs['llm_model']
        )
        
    # Update model list when provider changes
    def update_model_choices(provider):
        return gr.update(choices=get_models(provider))

    with gr.Blocks() as interface:
        gr.Markdown("## AgentWriting: AI Writing Assistant")
        
        with gr.Row():

            input_instruction = gr.Textbox(
                label="Enter Writing Instruction", 
                lines=2, 
                placeholder="Type the writing prompt or instruction here."
            )
            input_steps = gr.Slider(
                label="Number of Steps", 
                minimum=0, 
                maximum=4, 
                step=1, 
                value=0, 
                info="Specify how many steps the writing process should take."
            )
            
            # Dropdown for selecting the LLM provider
            input_llm_provider = gr.Dropdown(
                label="Select LLM Provider", 
                choices=llm_options, 
                value="GROQ", 
                info="Select the LLM provider."
            )
            
            if input_llm_provider.value == "Ollama":
                input_llm_model = gr.Dropdown(
                label="Select LLM Model", 
                choices=get_ollama_models,  # Default model list
                value="Default", 
                info="Select the model to use.",
                allow_custom_value=True  # Allow custom models not in the list
            )
            else:
                input_llm_model = gr.Dropdown(
                label="Select LLM Model", 
                choices=get_models("GROQ"),  # Default model list
                value="Default", 
                info="Select the model to use.",
                allow_custom_value=True  # Allow custom models not in the list
            )

        output_box = gr.Textbox(
            label="Generated Output", 
            lines=20, 
            placeholder="Your generated writing will appear here."
        )
        
        time_box = gr.Textbox(
            label="Generation Time", 
            lines=1, 
            placeholder="The time taken to generate the output will appear here."
        )

        wordcount_box = gr.Textbox(
            label="Word Count", 
            lines=1, 
            placeholder="The number of words used in the generated response."
        )


        # Update the model dropdown based on the selected provider
        input_llm_provider.change(
            fn=update_model_choices, 
            inputs=input_llm_provider, 
            outputs=input_llm_model
        )

        # Button to trigger writing generation
        generate_button = gr.Button("Generate")

        # Button to regenerate the output
        regenerate_button = gr.Button('\U0001f504 Regenerate', variant='secondary', elem_classes='refresh_button')

        # Connect the generate button to the on_generate_writing function
        generate_button.click(
            on_generate_writing,
            inputs=[input_instruction, input_steps, input_llm_provider, input_llm_model],
            outputs=[output_box, time_box, wordcount_box]
        )

        # Connect the regenerate button to the on_regenerate_writing function
        regenerate_button.click(
            on_regenerate_writing,
            outputs=[output_box, time_box, wordcount_box]
        )

    return interface


# Launch the Gradio app
if __name__ == "__main__":
    gradio_app().launch()
