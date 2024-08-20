from model.react import ollama_model_api, openai_model_api
import os
import sys
import json
import re

# Set directory paths
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
parent_directory = os.path.dirname(current_directory)

if parent_directory not in sys.path:
    sys.path.append(parent_directory)


# Define supported model APIs
SUPPORTED_MODEL_APIS = {
    "ollama_model_api": ollama_model_api.OllamaAPI,
    "openai_model_api": openai_model_api.OpenaiAPI,
}

class Agent:
    def __init__(self, model_type, model_name, system_prompt, ai_tools=None, use_generate=False):
        self.model_type = SUPPORTED_MODEL_APIS.get(model_type)
        if not self.model_type:
            raise ValueError(f"Unsupported model API: {model_type}")
        
        self.model_name = model_name
        self.use_generate = use_generate  # Flag to determine which API method to use
        self.model_instance = self.model_type(
            model=self.model_name, system=system_prompt)

    def execute_prompt(self, prompt):
        if self.use_generate:
            # Use the generate endpoint if the flag is set
            agent_response_str = self.model_instance.generate(prompt)
        else:
            # Use the chat endpoint by default
            agent_response_str = self.model_instance.chat(prompt)

        try:
            agent_response_dict = json.loads(agent_response_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON response: {e}")

        func_name = agent_response_dict.get('tool_choice')
        func_input_str = agent_response_dict.get('tool_input')

        if func_name == "no tool":
            return agent_response_dict
        elif func_name and func_input_str:
            return self.execute_function(func_name, func_input_str)
        else:
            return agent_response_dict

    def execute_function(self, func_name, input_str):
        if not self.ai_tools:
            raise ValueError("AI tools are not provided.")
        
        try:
            return self.ai_tools.execute_function(func_name, input_str)
        except Exception as e:
            raise ValueError(f"Error executing function '{func_name}': {e}")


# class Agent:
#     def __init__(self, model_type, model_name, system_prompt, ai_tools):
#         self.model_type = SUPPORTED_MODEL_APIS.get(model_type)
#         if not self.model_type:
#             raise ValueError(f"Unsupported model API: {model_type}")
#         self.model_name = model_name
#         self.ai_tools = ai_tools
#         self.agent_system_prompt = system_prompt.format(tool_descriptions=self.ai_tools.list_functions())
#         self.model_instance = self.model_type(model=self.model_name, system=self.agent_system_prompt)

#     def execute_prompt(self, prompt):

#         agent_response_str = self.model_instance.chat(prompt)

#         try:
#             agent_response_dict = json.loads(agent_response_str)
#         except json.JSONDecodeError as e:
#             raise ValueError(f"Error parsing JSON response: {e}")

#         func_name = agent_response_dict.get('tool_choice')
#         func_input_str = agent_response_dict.get('tool_input')

#         print(agent_response_dict)

#         if func_name == "no tool":
#             return agent_response_dict
#         elif func_name and func_input_str:
#             return self.execute_function(func_name, func_input_str)
#         else:
#             return agent_response_dict

#     def execute_function(self, func_name, input_str):
#         try:
#             return self.ai_tools.execute_function(func_name, input_str)
#         except Exception as e:
#             raise ValueError(f"Error executing function '{func_name}': {e}")
