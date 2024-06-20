import os
import sys

# Set directory paths
parent_dir = os.path.abspath('.')
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from model_api import ollama_model_api, openai_model_api
from ai_assistants.assistants_registry import get_functions_list

class Agent:
    def __init__(self, model_api, model_name):
        self.model_api = model_api
        self.model_name = model_name

    def execute_prompt(self, prompt):
        # Determine which model class to instantiate based on self.model_api
        if self.model_api == ollama_model_api:
            model_class = ollama_model_api.OllamaAPI
        elif self.model_api == openai_model_api:
            model_class = openai_model_api.OpenaiAPI
        else:
            raise ValueError(f"Unsupported model API: {self.model_api}")

        # Instantiate the model class
        model_instance = model_class(
            model=self.model_name,
        )

        # Generate and return the response dictionary
        agent_response_dict = model_instance.chat(prompt)
        return agent_response_dict

if __name__ == "__main__":
    model_api = ollama_model_api
    model_name = 'mistral:latest'
    stop = ""

    agent = Agent(model_api=model_api, model_name=model_name)
    response = agent.execute_prompt('What is capital of the united states?')
    print(response)