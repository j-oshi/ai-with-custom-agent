import os
import sys
import json

# Set directory paths
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
parent_directory = os.path.dirname(current_directory)
if parent_directory not in sys.path:
    sys.path.append(parent_directory)

from model.standard import ollama_model_api, openai_model_api
from prompts.modify_prompt import system_prompt_template 
from registry.tools_loader import loader

# Define supported model APIs (assuming these are defined elsewhere)
SUPPORTED_MODEL_APIS = {
    "ollama_model_api": ollama_model_api.OllamaAPI,
    "openai_model_api": openai_model_api.OpenaiAPI,
}

class Agent:
    def __init__(self, model_api_key, model_name, ai_tools):
        self.model_api = SUPPORTED_MODEL_APIS.get(model_api_key)
        if not self.model_api:
            raise ValueError(f"Unsupported model API: {model_api_key}")
        self.model_name = model_name
        self.ai_tools = ai_tools

    def execute_prompt(self, prompt):
        ai_tools = self.ai_tools.list_functions()
        agent_system_prompt = system_prompt_template.format(tool_descriptions=ai_tools)
        model_instance = self.model_api(
            model=self.model_name, 
            prompt_modification=agent_system_prompt
        )

        agent_response_str = model_instance.generate(prompt)

        try:
            agent_response_dict = json.loads(agent_response_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON response: {e}")

        func_name = agent_response_dict.get('tool_choice')
        func_input_str = agent_response_dict.get('tool_input')
        
        # If 'tool_choice' or 'tool_input' do not exist, return the response
        if func_name and func_input_str:
            return self.execute_function(func_name, func_input_str)

        # If 'tool_choice' is "no tool", return 'tool_input'
        if func_name == "no tool":
            return func_input_str
        else:
            return agent_response_dict
            

    def execute_function(self, func_name, input_str):
        try:
            return self.ai_tools.execute_function(func_name, input_str)
        except Exception as e:
            raise ValueError(f"Error executing function '{func_name}': {e}")

if __name__ == "__main__":
    model_api_key = "ollama_model_api"
    model_name = "mistral:latest"
    ai_tools = loader()

    agent = Agent(
        model_api_key=model_api_key,
        model_name=model_name,
        ai_tools=ai_tools,
    )

    while True:
        prompt = input("Enter prompt here: ")
        if prompt.lower() == "exit":
            break
    
        try:
            response = agent.execute_prompt(prompt)
            print(response)
        except ValueError as e:
            print(f"An error occurred: {e}")


