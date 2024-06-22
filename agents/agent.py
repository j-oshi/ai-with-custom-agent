import os
import sys
import json
from importlib import import_module

# Set directory paths
parent_dir = os.path.abspath('.')
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from prompts.modify_prompt import system_prompt_template
from model_api import ollama_model_api, openai_model_api
from registry.ai_assistants_registry import registry as registered_ai_assistants

# from ai_assistants.assistants_registry import get_functions_list
# from ai_assistants.assistants.financial.fixed_rate import fixed_rate_prompt

# Define supported model APIs (assuming these are defined elsewhere)
SUPPORTED_MODEL_APIS = {
    "ollama_model_api": ollama_model_api.OllamaAPI,
    "openai_model_api": openai_model_api.OpenaiAPI,
}


class Agent:
    def __init__(self, model_api_key, model_name, ai_assistants):
        self.model_api = SUPPORTED_MODEL_APIS.get(model_api_key)
        if not self.model_api:
            raise ValueError(f"Unsupported model API: {model_api_key}")
        self.model_name = model_name
        self.ai_assistants = ai_assistants

    def execute_prompt(self, prompt):
        ai_assistants = self.ai_assistants.list_functions()
        agent_system_prompt = system_prompt_template.format(tool_descriptions=ai_assistants)

        model_instance = self.model_api(
            model=self.model_name, prompt_modification=agent_system_prompt
        )

        agent_response_str = model_instance.chat(prompt)

        try:
            agent_response_dict = json.loads(agent_response_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON response: {e}")

        func_name = agent_response_dict['tool_choice']
        func_input_str = agent_response_dict['tool_input']

        if func_name == "no tool":
            return func_input_str
        else:
            return self.execute_function(func_name, func_input_str)

    def execute_function(self, func_name, input_str):
        return self.ai_assistants.execute_function(func_name, input_str)
        # Use import_module for dynamic tool loading
        # for tool in self.tools:
        #     if tool.__name__ == func_name:
        #         return tool(input_str)
        # # Raise an error if no matching tool is found
        # raise ValueError(f"Function not found: {func_name}")


if __name__ == "__main__":
    model_api_key = "ollama_model_api"  # Assuming this is the chosen API
    model_name = "mistral:latest"
    ai_assistants = registered_ai_assistants

    agent = Agent(
        model_api_key=model_api_key,
        model_name=model_name,
        ai_assistants=ai_assistants,
    )
    # response = agent.execute_prompt('What is capital of the united states?')
    # response = agent.execute_prompt(
    #     "If a principal amount of $5000 is invested at a fixed annual interest rate of 2.5% for a period of 3 years, what is the totalCostOfMortgage?"
    # )
    # print(response)

    while True:
        prompt = input("Enter prompt here: ")
        if prompt.lower() == "exit":
            break
    
        response = agent.execute_prompt(prompt)
        print(response)

