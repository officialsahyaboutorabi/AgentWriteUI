### Known Errors

# Sometimes Errors in this software may occur. In case they do, we have solutions for some of these known errors.

Error 1: You may encounter this error while opening the app.
```python
ImportError: cannot import name 'tool_call_chunk' from 'langchain_core.messages.tool' (/home/user/miniconda3/envs/agentwrite/lib/python3.11/site-packages/langchain_core/messages/tool.py)
```
The solution to this error:
```bash
pip uninstall langchain langchain-core langchain-openai
pip install langchain==0.2.7 langchain-core==0.2.15 langchain-openai==0.1.15
```

Error 2: You may encounter this error when trying to execute an instruction
```
Error during workflow execution: Error code: 404 - {'error': {'message': 'The model llama3:latest does not exist or you do not have access to it.', 'type': 'invalid_request_error', 'code': 'model_not_found'}}
```

The solution:

Run this command:
```
ollama list
```

Check to see if the model you wish to use exists:
```
NAME                            ID              SIZE    MODIFIED
minicpm-v:latest                1862d7d5fee5    5.5 GB  5 days ago
llava:7b                        8dd30f6b0cb1    4.7 GB  7 days ago
dolphin-mixtral:latest          cfada4ba31c7    26 GB   4 months ago
mxbai-embed-large:latest        468836162de7    669 MB  4 months ago
llama3:latest                   a6990ed6be41    4.7 GB  4 months ago
```

If you have the model you want to use, just press the `Generate` button again and it will be solved.

However if you don't see the model you want to use in your list then you can either choose a different model you already have.
Alternatively if you want to use a model you don't currently have installed, run the following command:
```
ollama pull nameofyourmodel
```

After your preferred model is installed, you can now use it.

Error 3: You may encounter this error also when opening the app.
```python
ImportError: cannot import name 'CONFIG_KEYS' from 'langchain_core.runnables.config' (/home/user/miniconda3/envs/agentwrite/lib/python3.11/site-packages/langchain_core/runnables/config.py)
```

Solution: Run the following command below
```
pip install langchain --upgrade
```

After running the command. Reopen the UI and it will fix the issue.
