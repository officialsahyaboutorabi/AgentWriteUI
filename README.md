<br/>

<h1 align="center">
    AgentWrite LangGraph UI
</h1>

<p align="center">
    AgentWrite LangGraph UI is an interface which allows you to use AgentWrite inside an interface.
    <br/>
    It is designed to create an advanced writing assistant powered by language models and graph-based workflows using a UI interface.
</p>

## Description

This project leverages LangGraph to orchestrate a series of language model interactions, creating a powerful tool for automated content generation. It breaks down complex writing tasks into manageable steps, including planning, writing, and refining content.

## Features

- [x] Automated content planning
- [x] Paragraph-by-paragraph content generation
- [x] Integration with multiple language models (OpenAI, GROQ, OLLaMA)
- [x] Flexible workflow management using LangGraph
- [x] Markdown output for generated content
- [x] Working User Interface to generate content
- [x] (BRAND NEW 🎉): Image-To-Story Generation (OLLaMA only)

## Installation

1. Clone the repository
   ```
   git clone https://github.com/officialsahyaboutorabi/AgentWriteUI.git
   ```

2. Navigate into the main directory:
   ```
   cd AgentWriteUI
   ```

3. Create a new conda environment. You must have miniconda installed.
   
   Install Miniconda here if you don't have it already: [Miniconda Installation](https://docs.anaconda.com/miniconda/miniconda-install/)

   If you have it already, create the new environment using the command below:

   ```
   conda create -n agentwrite python=3.11
   ```

   Then activate your conda environment after it has been setup by running the following command below:

   ```
   conda activate agentwrite
   ```


5. Once you have created your conda environment, you must install the dependencies:

   ```
   pip install -r requirements.txt
   ```



## Usage

BEFORE YOU START (you must be inside this folder AgentWriteUI)

Proceed directly to step 4 if you wish to use Ollama only, although it is highly recommended to create a `.env` file just incase you wish to use GROQ or OpenAI.

1. You must create a `.env` file by running this command:
   ```
   cat > .env
   ```
   After you run the command, paste the following in the next line and replace both placeholders with your actual API keys.
   ```
   OPENAI_API_KEY="REPLACE WITH YOUR OPENAIAPIKEY"
   GROQ_API_KEY="REPLACE WITH YOUR GROQAPIKEY"
   ```
   Then you press enter and it will write it in the file.

   However if you do not have either of those keys, you may get keys from both websites:
   [OpenAI API Key](https://platform.openai.com/api-keys)
   [GROQ API Key](https://console.groq.com/keys)

   If you don't have an account with either of the services listed above, you may need to sign up for an account.

3. Set up your environment variables by running these commands:
   ```
   export OPENAI_API_KEY="REPLACE WITH YOUR OPENAIAPIKEY"
   export GROQ_API_KEY="REPLACE WITH YOUR GROQAPIKEY"
   ```
   Once you finished setting up the `.env` file, save the file and then you can move onto the next step.

4. Run the main script:
   ```
   python main.py
   ```

## If you wish to close and reopen the UI, do the following.

1. Run this command. Make sure you replace the port with the port you are hosting this program in. To find your port, after running the `main.py` file, see Step 2.
   ```bash
   fuser -k 8501/tcp
   ```

   And then after, re-run the main script:
   ```
   streamlit run main.py
   ```
2. You should see the following after running the command:

   ```
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   Network URL: http://172.31.61.124:8501
   ```
   You must view your application in the Local URL.

## OPENAI

> [!WARNING]
> For any user who doesn't have a GPT-Plus subscription, they will not be able to use `gpt-4`. They are only able to use `gpt-3.5-turbo`.

## OLLAMA

> [!WARNING]
> If you wish to generate writing locally with Ollama models, you must have Ollama installed on your system or it will not work.
> Only text-generation models will work at the moment. However we will add new capabilities so stay tuned! (UPDATE, THE IMAGE READING MODEL `llava` NOW WORKS)

> [!TIP]
> To install Ollama on your system, go directly to the [Ollama Website](https://ollama.com/download)


## Image-to-Story Generation Released

> [!TIP]
> 🎉 We have finally released our software with Image-To-Story feature
> However it only works with `Ollama` at the moment.

## Story-to-Image Generation Released

> [!TIP]
> 🎉 We have finally released our software with Story-To-Image Generation feature
> However it only works with `OpenAI` at the moment and only the model `dall-e-3`.


## FAQ

> [!TIP]
> Q: Where can I see the results of the text generation?
> A: In the UI, it will show you the generated text as well as an exported .md file which is created in your local directory inside the AgentWriteUI file.


### Using the Test Branch

> [!WARNING]
> The `:test` branch has the latest unstable features and changes. Use it at your own risk as it may have bugs or incomplete features.

If you want to try out new experimental features, you can use the `:test` tag like this:



## Plans for the Future

### We always look to update this software. We plan to add:

- [x] Image-To-Story Generation (COMPLETED)
- [x] Multiple Languages in the Interface (German, Japanese and many more languages)
- [x] Story-To-Image Generation (COMPLETED)

## Troubleshooting Errors

Please see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for more information.

