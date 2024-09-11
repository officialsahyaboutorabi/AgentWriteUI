# AgentWrite LangGraph UI

AgentWrite LangGraph is an interface for the use of AgentWrite which uses LangGraph, designed to create an advanced writing assistant powered by language models and graph-based workflows using a UI interface.

## Description

This project leverages LangGraph to orchestrate a series of language model interactions, creating a powerful tool for automated content generation. It breaks down complex writing tasks into manageable steps, including planning, writing, and refining content.

## Features

- Automated content planning
- Paragraph-by-paragraph content generation
- Integration with multiple language models (OpenAI, GROQ, OLLaMA)
- Flexible workflow management using LangGraph
- Markdown output for generated content
- Working User Interface to generate content


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
   ```
   Install Miniconda here if you don't have it already: https://docs.anaconda.com/miniconda/miniconda-install/
   ```

   If you have it already, create the new environment using the command below:

   ```
   conda create -n agentwrite python=3.11
   ```

   Then activate your conda environment after it has been setup by running the following command below:

   ```
   conda activate agentwrite
   ```


4. Once you have created your conda environment, you must install the dependencies:

   ```
   pip install -r requirements.txt
   ```



## Usage

BEFORE YOU START (you must be inside this folder AgentWriteUI)

1. You must create a `.env` file by running this command:
   ```
   cat > .env
   ```
   After you run the command, paste the following in the next line.
   ```
   OPENAI_API_KEY="REPLACE WITH YOUR OPENAIAPIKEY"
   GROQ_API_KEY="REPLACE WITH YOUR GROQAPIKEY"
   ```
   Then you press enter and it will write it in the file.

2. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY="REPLACE WITH YOUR OPENAIAPIKEY"
   GROQ_API_KEY="REPLACE WITH YOUR GROQAPIKEY"
   ```
   Once you finished setting up the `.env` file, save the file and then you can move onto the next step.

3. Run the main script:
   ```
   python main.py
   ```





