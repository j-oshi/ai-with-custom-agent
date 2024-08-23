from agents.reactAgent import Agent
from registry.tools_loader import loader


def run_agent_until_answer(agent, question, max_turns=1):
    """
    Run the agent in a loop until a 'Final Answer' is found or the maximum number of turns is reached.

    Parameters:
    - agent: The agent instance to execute prompts.
    - question: The initial question or prompt to the agent.
    - max_turns: The maximum number of turns to attempt (default is 1).

    Returns:
    - result: The final result from the agent, or an error if something goes wrong.
    """
    next_prompt = question
    i = 0

    while i < max_turns:
        i += 1
        result = agent.execute_prompt(next_prompt)

        if isinstance(result, Exception):
            print("Error:", result)
            return result

        next_prompt = f"Observation: {result}"

        # Check if the result contains the 'Final Answer'
        if isinstance(result, dict) and 'Final Answer' in str(result):
            return result
        # else:
        #     i = 0
    return result  # Return the last result if no final answer is found

system_prompt_template = """ 
As a Data Analyst, when presented with a user query, your task will involve:

- Determining if the question needs to be broken down into smaller parts for a more accurate answer.
- Solving each part to arrive at a comprehensive answer.

Detail the approach to solving each part in bullet points. If some information is unavailable or unreliable, list the required information and note any limitations in bullet points.

- Questions: Bullet points of questions.
- Details: Describe questions.

You will generate the following JSON response:

"tool_choice": "name_of_the_tool",
"tool_input": "inputs_to_the_tool"

- `tool_choice`: The name of the tool you want to use. It must be a tool from your toolbox 
                or "no tool" if you do not need to use a tool.
- `tool_input`: The specific inputs required for the selected tool. 
                If no tool, just provide a response to the query.

Here is a list of your tools along with their descriptions:
{tool_descriptions}

Please make a decision based on the provided user query and the available tools.
"""

if __name__ == "__main__":
    model_type = "ollama_model_api"
    model_name = "mistral-nemo:latest"
    # model_name = "mistral:latest"
    # model_name = "phi3:medium" 
    ai_tools = loader()

    agent = Agent(
        model_type=model_type,
        model_name=model_name,
        system_prompt=system_prompt_template,
        ai_tools=ai_tools,
        use_generate=True
    )

    while True:
        question = input("Enter question here (type 'exit' to quit): ")
        if question.lower() == "exit":
            break

        # next_prompt = question
        # max_turns = 1
        # i = 0

        result = run_agent_until_answer(agent, question, max_turns=1)
        if not result:
            continue

        print(result)


# Questions to ask
# Get a list of software companies that begin with the letter 's'.
# Get list of software comp-anies that have names that start with b
# How many companies are in table software_company?
# Retrieve a list of software company names that begin with either the letter ‘A’ or ‘S’. The list should only include the name and postcode of each company

# is to determine if the question needs to be broken down into smaller parts.


#  agent with access to a registry of useful functions. Given a user query, 
# you will determine which functions, if any, is best suited to answer the query. Analyse the output and give a summary.