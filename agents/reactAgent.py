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

from prompts.modify_prompt import system_prompt_template
from registry.register_tools import create_registry as registered_ai_assistants
from model.react import ollama_model_api, openai_model_api

# Define supported model APIs
SUPPORTED_MODEL_APIS = {
    "ollama_model_api": ollama_model_api.OllamaAPI,
    "openai_model_api": openai_model_api.OpenaiAPI,
}


class Agent:
    def __init__(self, model_type, model_name, system_prompt, ai_assistants):
        self.model_type = SUPPORTED_MODEL_APIS.get(model_type)
        if not self.model_type:
            raise ValueError(f"Unsupported model API: {model_type}")
        self.model_name = model_name
        self.ai_assistants = ai_assistants
        self.agent_system_prompt = system_prompt.format(tool_descriptions=self.ai_assistants.list_functions())
        self.model_instance = self.model_type(model=self.model_name, system=self.agent_system_prompt)

    def execute_prompt(self, prompt):

        agent_response_str = self.model_instance.chat(prompt)

        try:
            agent_response_dict = json.loads(agent_response_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON response: {e}")

        func_name = agent_response_dict.get('tool_choice')
        func_input_str = agent_response_dict.get('tool_input')

        if func_name and func_input_str:
            return self.execute_function(func_name, func_input_str)
        elif func_name == "no tool":
            print('No tool response')
            print(agent_response_dict)
            print('End of no tool response')
            return func_input_str
        else:
            return agent_response_dict

    def execute_function(self, func_name, input_str):
        try:
            return self.ai_assistants.execute_function(func_name, input_str)
        except Exception as e:
            raise ValueError(f"Error executing function '{func_name}': {e}")


prompt_template = """
You are an agent with access to a registry of useful functions. 
Given a user query, you will determine which functions, if any, are best suited to answer the query.

You will generate the following JSON response:

"tool_choice": "name_of_the_tool",
"tool_input": "inputs_to_the_tool",

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

    agent = Agent(
        model_type=model_type,
        model_name=model_name,
        system_prompt=prompt_template,
        ai_assistants=ai_assistants
    )

    while True:
        question = input("Enter question here (type 'exit' to quit): ")
        if question.lower() == "exit":
            break

        next_prompt = question
        max_turns = 1
        i = 0

        while i < max_turns:
            i += 1
            result = agent.execute_prompt(next_prompt)

            if isinstance(result, Exception):
                print("Error:", result)
                break 

            print("Observation:", result)
            next_prompt = f"Observation: {result}"

            if 'answer' in result:  # Custom logic to check for an answer in the observation
                print("Answer:", result)
                break
            else:
                i = 0

        print('End of execution for this query.')

print('Program terminated.')

# How much will be paid monthly on a loan of £10000 for 5 years at a interest rate of 2.5% per year. What is the total amount paid after 5 years?
