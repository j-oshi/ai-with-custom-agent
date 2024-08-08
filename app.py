from agents.reactAgent import Agent
from registry.tools_loader import loader
# from prompts.modify_prompt import test_prompt_template
from prompts.prompt_builder import PromptBuilder

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

        # print("Observation:", result)
        next_prompt = f"Observation: {result}"

        # Check if the result contains the 'Final Answer'
        if isinstance(result, dict) and 'Final Answer' in str(result):
            # print("Answer:", result)
            return result

        # Reset the turn counter if further processing is needed
        i = 0

    # print('End of execution for this query.')
    return result  # Return the last result if no final answer is found


prompt_template = """
**Task:** Extract relevant data from a given query based on provided categories, object properties, and example data.

**Process:**

1. **Thought:** Consider the query and its potential meaning.
2. **Action:** Analyze the query for keywords or phrases related to business operations.
3. **PAUSE:** Halt the process temporarily to ensure a thorough review.
4. **Observation:** Determine if the query aligns with a business operation problem based on the analysis.
5. **Answer:** Provide a final answer indicating whether the query is a business operation problem and, if so, extract the relevant data.

**Categories:**
* **Startup Investments:** Loan Amount, Interest Rate, Loan Duration, Equipment Cost, Other Investment Costs
* **Fixed Costs:** Rent, Utilities, Wages, Insurance, Other Fixed Costs
* **Variable Costs:** Raw Materials, Packaging, Shipping, Sales Commission, Other Variable Costs
* **Revenue:** Unit Sales, Unit Price, Subscription Revenue, Discounts, Other Revenue Streams

**Object Properties:**
* **category:** Startup Investments, Fixed Costs, Variable Costs, Revenue
* **type:** Specific type within category
* **name:** Item or investment name
* **detail:** Additional description
* **amount:** Total monetary value
* **quantity:** Item quantity
* **unit_info:** Unit details
* **unit:** Measurement unit
* **billing_frequency:** Billing frequency
* **amount_per_unit:** Amount per unit
* **interest_rate:** Interest rate
* **term_years:** Loan term
* **currency:** Currency
* **working_time:** Labor time

**Example Data:**
{example}

**Extraction Process:**
1. **Analyze:** Examine the query for specific terms or phrases that match the categories and object properties. For example, terms like "monthly costs," "rent," "utilities," etc.
2. **Map:** Attempt to align the identified terms with the predefined schema. This includes associating them with the correct category, type, and property values.
3. **Extract:** Once mapped, extract the relevant data points that fit within the given framework.
4. **Validate:** Cross-check the extracted data against the example data to ensure accuracy and relevance.

**Example Query and Extraction:**
* **Query:** "What are the monthly costs for rent and utilities?"
* **Thought:** The query seeks information about fixed costs related to rent and utilities.
* **Action:** Identify the relevant categories (Fixed Costs) and specific items (Rent, Utilities).
* **Observation:** Determine if the amounts for rent (£2,500) and utilities (£400) are available.
* **Answer:** Extract and format the data:
  * Output: `Final Answer: {schema}

**Additional Considerations:**
* **Ambiguous Queries:** For queries that are unclear or could belong to multiple categories, clarify the context or provide a range of possible interpretations.
* **Complex Queries:** Break down complex queries into smaller parts to ensure accurate extraction.
* **Data Cleaning:** Normalize extracted data for consistency (e.g., currency conversions, unit standardization).
* **Error Handling:** If the query is invalid or the data is missing, return a meaningful error message that guides the user.

**Final Notes:**
- The process should focus on precise and relevant data extraction, ensuring that the extracted data directly answers the query within the framework provided.
- Use the example data as a reference point for validating extracted information.

"""

example_description = """
A business secured a £50,000 loan at 9.8% interest for 2 years to purchase equipment. Additional expenditures of £10,000 and £8,000 were for a food mixer and dough moulder, respectively. Monthly costs include £2,500 rent, £400 electricity, £4,500 for three workers (each earning £1,500), and £2,250 for a supervisor. Daily variable costs are £400 for flour (20 x 16kg bags at £20/bag), £10 for salt (5 x 1.5kg bags at £2/bag), and £75 for yeast (5 x 1kg bags at £15/bag). The business produces 600 loaves daily, selling each for £1.89. Projected monthly sales are 18,000 loaves, with additional £500 monthly subscription revenue and £50 in discounts.
"""

business_output_schema = [{"category": "fixedCosts", "name": "Rent", "amount": 2500}, {"category": "fixedCosts", "name": "Utilities", "amount": 400}]

if __name__ == "__main__":
    model_type = "ollama_model_api"
    model_name = "mistral:latest"
    ai_tools = loader()
    prompt_builder = PromptBuilder(
        schema=business_output_schema,
        example=example_description,
        tool_descriptions=ai_tools,
        prompt_template=prompt_template
    )

    final_prompt = prompt_builder.build_prompt()
    print(final_prompt)

    agent = Agent(
        model_type=model_type,
        model_name=model_name,
        system_prompt=final_prompt,
        ai_tools=ai_tools
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
        # while i < max_turns:
        #     i += 1
        #     result = agent.execute_prompt(next_prompt)

        #     if isinstance(result, Exception):
        #         print("Error:", result)
        #         break

        #     print("Observation:", result)
        #     next_prompt = f"Observation: {result}"

        #     # if isinstance(result, str) and 'answer' in result:
        #     if isinstance(result, dict) and 'Final Answer' in str(result):
        #         print("Answer:", result)
        #         break
        #     else:
        #         i = 0

        # print('End of execution for this query.')

print('Program terminated.')
