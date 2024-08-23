import os
import sys
import json
from model.react import ollama_model_api, openai_model_api

# Set directory paths and update the system path if necessary
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
    """
    The Agent class is responsible for interacting with a specified model API
    and executing AI tools as necessary based on the model's response.

    Attributes:
        model_type (class): The class representing the model API to use.
        model_name (str): The name of the specific model instance to use.
        system_prompt (str): The initial prompt to be provided to the model.
        ai_tools (object): An optional object containing AI tools that can be invoked.
        use_generate (bool): Determines whether to use the 'generate' or 'chat' method.
        model_instance (object): The instantiated model API object.
    """

    def __init__(self, model_type, model_name, system_prompt, ai_tools=None, use_generate=False):
        """
        Initializes the Agent with the specified model type, model name, and system prompt.

        Args:
            model_type (str): The key for the model type, which must be in SUPPORTED_MODEL_APIS.
            model_name (str): The name of the model to be used.
            system_prompt (str): The system prompt template.
            ai_tools (object, optional): An object containing AI tools.
            use_generate (bool, optional): Flag to determine which API method to use.

        Raises:
            ValueError: If an unsupported model type is provided.
        """
        model_class = SUPPORTED_MODEL_APIS.get(model_type)
        if not model_class:
            raise ValueError(f"Unsupported model API: {model_type}")

        self.model_name = model_name
        self.use_generate = use_generate
        self.ai_tools = ai_tools

        formatted_prompt = system_prompt.format(
            tool_descriptions=ai_tools.list_functions()) if ai_tools else system_prompt

        self.model_instance = model_class(
            model=self.model_name, system=formatted_prompt)

    def execute_prompt(self, prompt):
        """
        Executes a given prompt using the model's API and optionally invokes AI tools based on the response.

        Args:
            prompt (str): The user prompt to be processed by the model.

        Returns:
            dict: The JSON-decoded response from the model or the result from executing an AI tool.

        Raises:
            ValueError: If there is an error parsing the JSON response or executing a tool.
        """
        agent_response_str = self.model_instance.generate(
            prompt) if self.use_generate else self.model_instance.chat(prompt)

        try:
            agent_response_dict = json.loads(agent_response_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON response: {e}")

        func_name = agent_response_dict.get('tool_choice')
        func_input_str = agent_response_dict.get('tool_input')

        print(func_name)
        print(func_input_str)
        if func_name == "no tool":
            return agent_response_dict
        elif func_name and func_input_str:
            return self.execute_function(func_name, func_input_str)
        else:
            return agent_response_dict

    def execute_function(self, func_name, input_str):
        """
        Executes a specified function from the AI tools.

        Args:
            func_name (str): The name of the function to execute.
            input_str (str): The input string for the function.

        Returns:
            The result of the function execution.

        Raises:
            ValueError: If AI tools are not provided or if there is an error executing the function.
        """
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
