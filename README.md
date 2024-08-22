# ai-with-custom-agent
Ai with custom agent to solve local task.

## Install ollama
Install and pull down model

## Api keys
Create .env file at root level and add api key for model.

## Load Database
Run py load_database.py to load example csv files into sql tables.

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
├─ .gitignore
├─ agents
│  └─ agent.py
├─ ai_assistants
│  ├─ financial
│  │  ├─ fixed_rate.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ config.yaml
├─ model_api
│  ├─ base_model_api.py
│  ├─ ollama_model_api.py
│  ├─ openai_model_api.py
│  └─ __init__.py
├─ notebooks
│  └─ ai-functions-analysis.ipynb
├─ prompts
│  ├─ modify_prompt.py
│  └─ __init__.py
├─ README.md
├─ registry
│  ├─ ai_assistants_registry.py
│  ├─ register_tools.py
│  └─ __init__.py
├─ requirements.txt
├─ tests
│  ├─ test_fixed_rate.py
│  └─ test_ollama_api.py
└─ utils
   ├─ config.py
   ├─ helpers.py
   └─ __init__.py

```