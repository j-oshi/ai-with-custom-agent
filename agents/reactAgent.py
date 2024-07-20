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
from registry.tools_loader import loader
from model.react import ollama_model_api, openai_model_api

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
        self.ai_tools = ai_tools
        self.agent_system_prompt = system_prompt.format(tool_descriptions=self.ai_tools.list_functions())
        self.model_instance = self.model_type(model=self.model_name, system=self.agent_system_prompt)

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

# Can put constraint by making prompt use only supplied tools
prompt_template = """
As an agent, when presented with a user query, your task is to determine if the question needs to be broken down into smaller parts. Detail your approach to solving each part in bullet points. If some information is unavailable or unreliable, list the required information and note the limitations in bullet points.

For each question, follow this process in a loop: Thought, Action, PAUSE, Observation.

- Thought: Describe your initial thoughts about the question, considering potential limitations in the available information.
- Action: Decide which function, if any, is best suited to answer the query reliably, and execute the function. Then, return PAUSE.
- Observation: Provide insight into the result from the action, including any limitations or potential inaccuracies.

At the end of the loop, output an Answer and move to the next question.

Once you have concluded all the questions, create a Final Answer, summarizing your conclusions in bullet points.

You have a set of useful functions at your disposal to solve the questions. Each function's usage is detailed in its docstring. You will generate the following JSON response:

"tool_choice": "name_of_the_tool",
"tool_input": "inputs_to_the_tool",

- `tool_choice`: The name of the tool you want to use (or "no tool" if no tool is suitable).
- `tool_input`: The specific inputs required for the selected tool. If no tool is needed, provide a response to the query, acknowledging potential limitations.

Here is a list of your tools along with their descriptions:
{tool_descriptions}
"""

if __name__ == "__main__":
    model_type = "ollama_model_api"
    model_name = "mistral:latest"
    ai_tools = loader()

    agent = Agent(
        model_type=model_type,
        model_name=model_name,
        system_prompt=prompt_template,
        ai_tools=ai_tools
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

            # if isinstance(result, str) and 'answer' in result:
            if 'Final Answer' in result:
                print("Answer:", result)
                break
            else:
                i = 0

        print('End of execution for this query.')

print('Program terminated.')

# How much will be paid monthly on a loan of £10000 for 5 years at a interest rate of 2.5% per year. What is the total amount paid after 5 years?
# Considering the total cost, is it cheaper to borrow £40,000 for 5 years at an interest rate of 2.5% per year or £35,000 for 6 years at an interest rate of 2% per year?
# automate http://demo.oshinit.com/