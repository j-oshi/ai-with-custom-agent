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

from model.react import ollama_model_api, openai_model_api
from prompts.modify_prompt import system_prompt_template 
from registry.register_tools import create_registry as registered_ai_assistants

# Define supported model APIs
SUPPORTED_MODEL_APIS = {
    "ollama_model_api": ollama_model_api.OllamaAPI,
    "openai_model_api": openai_model_api.OpenaiAPI,
}

# class Agent:
#     def __init__(self, model_api_key, model_name, ai_assistants):
#         self.model_api = SUPPORTED_MODEL_APIS.get(model_api_key)
#         if not self.model_api:
#             raise ValueError(f"Unsupported model API: {model_api_key}")
#         self.model_name = model_name
#         self.ai_assistants = ai_assistants

#     def execute_prompt(self, prompt):
#         ai_assistants = self.ai_assistants.list_functions()
#         agent_system_prompt = system_prompt_template.format(tool_descriptions=ai_assistants)
#         model_instance = self.model_api(
#             model=self.model_name, 
#             prompt_modification=agent_system_prompt
#         )

#         agent_response_str = model_instance.generate(prompt)

#         try:
#             agent_response_dict = json.loads(agent_response_str)
#         except json.JSONDecodeError as e:
#             raise ValueError(f"Error parsing JSON response: {e}")

#         func_name = agent_response_dict.get('tool_choice')
#         func_input_str = agent_response_dict.get('tool_input')
        
#         if func_name and func_input_str:
#             return self.execute_function(func_name, func_input_str)
        
#         if func_name == "no tool":
#             return func_input_str
#         else:
#             return agent_response_dict

#     def execute_function(self, func_name, input_str):
#         try:
#             return self.ai_assistants.execute_function(func_name, input_str)
#         except Exception as e:
#             raise ValueError(f"Error executing function '{func_name}': {e}")

prompt_template = """
You are an agent with access to a registry of useful functions. 
Given a user query, you will determine which functions, if any, are best suited to answer the query.

You will generate the following JSON response:

"tool_choice": "name_of_the_tool",
"tool_input": "inputs_to_the_tool"

- `tool_choice`: The name of the tool you want to use. It must be a tool from your toolbox or "no tool" if you do not need to use a tool.
- `tool_input`: The specific inputs required for the selected tool. If no tool, just provide a response to the query.

You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to decide which function, if any, is best suited to answer the query and run the functions - then return PAUSE.
Use Observation to provide insight into the result from action.

Here is a list of your tools along with their descriptions:
{tool_descriptions}
"""

if __name__ == "__main__":
    model_type = "ollama_model_api"
    model_name = "mistral:latest"
    ai_assistants = registered_ai_assistants()

    agent_system_prompt = prompt_template.format(tool_descriptions=ai_assistants.list_functions())
    bot = SUPPORTED_MODEL_APIS[model_type](model_name, agent_system_prompt)

    question = input("Enter question here: ")
    next_prompt = question
    max_turns = 5
    i = 0

    while i < max_turns:
        i += 1
        result = bot.chat(next_prompt)

        try:
            agent_response_dict = json.loads(result)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON response: {e}")

        func_name = agent_response_dict.get('tool_choice')
        func_input_str = agent_response_dict.get('tool_input')

        if func_name and func_input_str:
            observation = ai_assistants.execute_function(func_name, json.dumps(func_input_str))
        elif func_name == "no tool":
            observation = func_input_str
            print("Answer:", observation)
            break  # Terminate the loop if the answer is found
        else:
            observation = agent_response_dict

        print(f" -- running {func_name} {func_input_str}")
        print("Observation:", observation)
        next_prompt = f"Observation: {observation}"

        if 'answer' in observation:  # Custom logic to check for an answer in the observation
            print("Answer:", observation)
            break

    print('End of execution.')