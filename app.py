from agents.reactAgent import Agent 
from registry.tools_loader import loader
from prompts.modify_prompt import test_prompt_template

if __name__ == "__main__":
    model_type = "ollama_model_api"
    model_name = "mistral:latest"
    ai_tools = loader()

    agent = Agent(
        model_type=model_type,
        model_name=model_name,
        system_prompt=test_prompt_template,
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