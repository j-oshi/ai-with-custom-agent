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
    def __init__(self, model_type, model_name, system_prompt, ai_tools):
        self.model_type = SUPPORTED_MODEL_APIS.get(model_type)
        if not self.model_type:
            raise ValueError(f"Unsupported model API: {model_type}")
        self.model_name = model_name
        # self.ai_tools = ai_tools

        # Generate tool descriptions
        # tool_descriptions_list = self.ai_tools.list_functions()

        # if not isinstance(tool_descriptions_list, list):
            # raise ValueError(
            #     "Tool descriptions must be a list of dictionaries.")

        # Convert list of dictionaries to a formatted string
        # tool_descriptions = "\n".join(
        #     [f"Function: {tool['func_name']}\nDescription: {
        #         tool['docstring']}" for tool in tool_descriptions_list]
        # )

        # # Ensure the placeholder exists in the prompt
        # if "{tool_descriptions}" not in system_prompt:
        #     raise ValueError(
        #         "The system prompt is missing the '{tool_descriptions}' placeholder.")

        # Use string replacement
        # self.agent_system_prompt = system_prompt.replace(
        #     "{tool_descriptions}", tool_descriptions)
        self.model_instance = self.model_type(
            model=self.model_name, system=system_prompt)

    def execute_prompt(self, prompt):
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
