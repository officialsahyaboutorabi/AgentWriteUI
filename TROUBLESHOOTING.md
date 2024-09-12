### Known Errors

# Sometimes Errors in this software may occur. In case they do, we have solutions for some of these known errors.

1. Error 1
```python
ImportError: cannot import name 'tool_call_chunk' from 'langchain_core.messages.tool' (/home/user/miniconda3/envs/agentwrite/lib/python3.11/site-packages/langchain_core/messages/tool.py)
```
The solution to this error:
```bash
pip uninstall langchain langchain-core langchain-openai
pip install langchain==0.2.7 langchain-core==0.2.15 langchain-openai==0.1.15
```


2.Error 2: You may encounter this error when trying to execute an instruction
```
Error during workflow execution: Error code: 404 - {'error': {'message': 'The model llama3:latest does not exist or you do not have access to it.', 'type': 'invalid_request_error', 'code': 'model_not_found'}}
```

The solution is to press the `Generate` button again and it will be solved.
