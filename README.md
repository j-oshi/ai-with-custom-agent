# ai-with-custom-agent
Ai with custom agent to solve local task.

## Install ollama
Install and pull down model

## Run query 
Start by 
```bash
py agents/agent.py
```

## Running unittests
To run the tests, navigate to the root of your project in the terminal and run:
```bash
py -m unittest discover -s tests
```

## Folder structure
```
ai_with_custom_agent
├─ ai_assistants
│  ├─ assistanta.py
│  └─ assistants
│     └─ financial
│        └─ fixed_rate.py
├─ config.yaml
├─ model_api
│  ├─ base_model_api.py
│  ├─ ollama_model_api.py
│  ├─ openai_model_api.py
│  └─ __init__.py
├─ Notebooks
│  └─ ai-functions-analysis.ipynb
├─ README.md
├─ requirements.txt
├─ tests
│  └─ test_ollama_api.py
└─ utils
   ├─ config.py
   ├─ helpers.py
   └─ __init__.py
