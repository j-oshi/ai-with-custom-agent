from agents.reactAgent import Agent
from registry.tools_loader import loader
from prompts.prompt_builder import PromptBuilder
# from prompts.task_prompt.business_viability_prompts import business_data_extraction_prompt


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


if __name__ == "__main__":
    model_type = "ollama_model_api"
    # model_name = "mistral-nemo:latest"
    model_name = "mistral:latest"
    # model_name = "phi3:medium" 
    # model_name = "tinyllama:latest"
    ai_tools = loader()
    # prompt_builder = PromptBuilder(
    #     goal=business_goal,
    #     schema=business_output_schema,
    #     example=f'{example_description} \n {example_output}',
    #     tool_descriptions=ai_tools,
    #     prompt_template=prompt_template
    # )

    prompt_builder = """
    ### Task: Extract and Categorize Data Based on Framework

    **Process Overview:**

    1. **Understand the Query:**
    - **Identify:** Recognize keywords related to business operations.
    - **Interpret:** Analyze the context to determine relevance.
    - **Review:** Ensure completeness of the analysis.
    - **Determine:** Assess if the query relates to a business operation issue.

    2. **Responding to the Query:**
    - **Confirm:** Identify if the query pertains to a business operation problem.
    - **Extract:** If relevant, extract and categorize data according to the framework.
    - **Output:** Present the findings as the final answer.

    ### Categories and Types:

    1. **Startup Investments:**
    - **Description:** This category encompasses the initial capital and resources necessary to start a business. It includes funding, equipment purchases, and other initial expenditures.
    - **Type Descriptions:**
        - **loan:** Financial support provided by a lender that must be repaid with interest over a set period.
        - **equipment:** Physical assets purchased for business operations, such as machinery or technology.
        - **otherInvestment:** Any other form of investment used to establish the business, including property or initial inventory.

    2. **Fixed Costs:**
    - **Description:** Regular, recurring expenses that a business incurs regardless of its production levels or sales volume. These costs are essential for maintaining daily operations.
    - **Type Descriptions:**
        - **rent:** Regular payments for the use of business premises or equipment.
        - **utilities:** Ongoing expenses for essential services like electricity, water, and internet.
        - **wages:** Salaries paid to employees on a regular basis.
        - **insurance:** Costs associated with protecting the business from risks through insurance policies.
        - **otherFixedCost:** Any other recurring expense that does not vary with production or sales volume, such as maintenance fees.

    3. **Variable Costs:**
    - **Description:** Expenses that fluctuate in direct proportion to the production levels or sales volume of a business. These costs vary based on the amount of goods or services a business produces.
    - **Type Descriptions:**
        - **rawMaterials:** Costs for materials used directly in the production of goods.
        - **packaging:** Expenses related to packaging products for sale or shipment.
        - **shipping:** Costs incurred in transporting goods to customers or distributors.
        - **salesCommission:** Payments made to sales personnel based on their performance or sales volume.
        - **otherVariableCost:** Any other cost that fluctuates with production levels or sales volume, such as transaction fees.

    4. **Revenue:**
    - **Description:** The income generated from a business’s operational activities. This category includes all forms of earnings, from product sales to subscriptions and additional revenue streams.
    - **Type Descriptions:**
        - **unitSales:** Income generated from selling individual units of products or services.
        - **subscriptionRevenue:** Revenue earned from customers who pay regularly for continued access to products or services.
        - **discounts:** Reductions in revenue due to price discounts offered to customers.
        - **otherRevenue:** Any other income stream that does not fall into the above categories, such as rental income or licensing fees.

    ### Object Properties for Data Categorization:

    - **category:** The overarching category (e.g., startupInvestments, fixedCosts, variableCosts, revenue).
    - **type:** The specific type within the category.
    - **name:** The name of the item or investment.
    - **detail:** Additional context or description.
    - **amount:** The monetary value in decimal format.
    - **quantity:** The number of units or items.
    - **unit:** The measurement unit (e.g., hours, days, kg, l).
    - **unit_info:** Details about the unit of measurement.
    - **amount_per_unit:** The cost or quantity per unit (e.g., £20 per hour, 20 scones per hour).
    - **interest_rate:** Applicable interest rate for loans.
    - **term_years:** Loan term duration in years.
    - **currency:** The currency used.
    - **time_durations:** A list of dictionaries specifying the time_unit and duration, each representing the length or frequency of an activity within a given time frame. This captures how often or how long an activity occurs within a specific period (e.g., hours per day, days per week, weeks per month).
      - **time_unit:** The unit of time (e.g., hour, day, week), used to indicate the period over which an activity is measured.
      - **duration:** The number of time units within the specified period. For example, a contractor might work 8 hours per day, 4 days per week, 4 weeks per month, or a bakery might produce 20 scones per hour, 6 hours per day, 3 days per week.
    - **rate_per_unit:** The rate or amount associated with a specific unit of time or production (e.g., £20 per hour for a contractor, 20 scones per hour).
    - **billing_frequency:** How often the amount is paid. Use where time_durations cannot be used to capture data.

    ### Data Extraction Process:

    1. **Analyze:** Identify relevant terms in the query corresponding to categories, types, and properties.
    2. **Map:** Align identified terms with the correct categories, types, and properties from the framework.
    3. **Extract:** Retrieve data points matching the framework’s definitions.
    4. **Validate:** Cross-check the extracted data for accuracy and relevance.

    ### Additional Guidelines:

    - **Ambiguity:** Provide multiple interpretations if necessary.
    - **Complexity:** Break down complex queries into simpler parts.
    - **Normalization:** Standardize data (e.g., currency conversion, unit normalization).
    - **Error Handling:** Offer informative feedback if the query is unclear or incomplete.

    **Final Notes:**
    - Use the provided framework strictly for data extraction.
    - Ensure all category and type values match the given options.
    """

    example_prompt = """
    **Example Question:**
    A bakery took out a £65,000 loan at an interest rate of 8.5% over 3 years to purchase essential equipment. Additional funds totaling £22,000 were invested in a commercial oven, dough divider, and a proofer. Monthly overhead costs include £3,000 for rent, £550 for electricity, £5,200 for three employees’ wages, a contractor is paid £20 per hour, 8 hours per day, 4 days per week, 4 weeks per month, and £2,500 for a supervisor’s salary. Daily operational expenses consist of £450 for flour, £15 for salt, £80 for yeast, and £180 for packaging materials. The bakery produces 720 loaves of bread daily, selling each for £2.15. Additionally, the bakery sells 120 pastries daily at £1.50 each. Plus 20 scorns are produced hourly, 6 hours per day, 3 days per week and 2 weeks per month selling at £0.85 each.  

    **Example Extracted Data:**
    ```json
        {
        "Startup Investments":[
            {
                "category":"startupInvestments",
                "type":"loan",
                "name":"Business Loan",
                "detail":"£65,000 loan for purchasing equipment",
                "amount":65000,
                "currency":"GBP",
                "interest_rate":8.5,
                "term_years":3
            },
            {
                "category":"startupInvestments",
                "type":"otherInvestment",
                "name":"Commercial Equipment",
                "detail":"Commercial oven, dough divider, and proofer",
                "amount":22000,
                "currency":"GBP"
            }
        ],
        "Fixed Costs":[
            {
                "category":"fixedCosts",
                "type":"rent",
                "name":"Rent",
                "detail":"Monthly rent for the bakery premises",
                "amount_per_unit":3000,
                "unit":"GBP",
                "billing_frequency":"monthly"
            },
            {
                "category":"fixedCosts",
                "type":"utilities",
                "name":"Electricity",
                "detail":"Monthly electricity bill",
                "amount_per_unit":550,
                "unit":"GBP",
                "billing_frequency":"monthly"
            },
            {
                "category":"fixedCosts",
                "type":"wages",
                "name":"Employee Wages",
                "detail":"Monthly wages for three employees",
                "amount_per_unit":5200,
                "unit":"GBP",
                "billing_frequency":"monthly"
            },
            {
                "category":"fixedCosts",
                "type":"otherFixedCost",
                "name":"Contractor Labor",
                "detail":"Hourly labor cost for a contractor",
                "amount_per_unit":20,
                "unit":"GBP",
                "time_rate":"hourly",
                "perHour": 8,
                "perDay": 4,
                "perWeek": 4,
                "perMonth": 1,
            },
            {
                "category":"fixedCosts",
                "type":"otherFixedCost",
                "name":"Supervisor Salary",
                "detail":"Monthly salary for the supervisor",
                "amount_per_unit":2500,
                "unit":"GBP",
                "billing_frequency":"monthly"
            }
        ],
        "Variable Costs":[
            {
                "category":"variableCosts",
                "type":"rawMaterials",
                "name":"Flour",
                "detail":"Daily flour cost for bread production",
                "amount_per_unit":450,
                "unit":"GBP",
                "billing_frequency":"daily"
            },
            {
                "category":"variableCosts",
                "type":"otherVariableCost",
                "name":"Salt",
                "detail":"Daily salt cost for bread production",
                "amount_per_unit":15,
                "unit":"GBP",
                "billing_frequency":"daily"
            },
            {
                "category":"variableCosts",
                "type":"otherVariableCost",
                "name":"Yeast",
                "detail":"Daily yeast cost for bread production",
                "amount_per_unit":80,
                "unit":"GBP",
                "billing_frequency":"daily"
            },
            {
                "category":"variableCosts",
                "type":"otherVariableCost",
                "name":"Packaging Materials",
                "detail":"Daily packaging materials cost for bread production",
                "amount_per_unit":180,
                "unit":"GBP",
                "billing_frequency":"daily"
            }
        ],
        "Revenue":[
            {
                "category":"revenues",
                "type":"unitSales",
                "name":"Bread Sales",
                "detail":"Daily bread sales revenue",
                "amount_per_unit":2.15,
            "currency":"GBP",
            "quantity": 720,
                "unit":"scorn",
                "time_rate":"daily"
            },
            {
                "category":"revenues",
                "type":"unitSales",
                "name":"Pastry Sales",
                "detail":"Daily pastry sales revenue",
                "amount_per_unit": 1.50,
            "currency":"GBP",
            "quantity": 120,
                "unit":"pastry",
                "time_rate":"daily"
            },
            {
                "category":"revenues",
                "type":"otherSales",
                "name":"Scorns",
                "detail":"Scorns sales revenue",
                "amount_per_unit":0.85,
            "currency":"GBP",
                "unit":"scorn",
            "quantity": 20,
                "time_rate":"hourly",
                "perHour": 6,
                "perDay": 3,
                "perWeek": 2,
                "perMonth": 1,
            }
        ]
        }
    ```
    """

    agent = Agent(
        model_type=model_type,
        model_name=model_name,
        system_prompt=prompt_builder,
        ai_tools=ai_tools
    )

    while True:
        question = input("Enter question here (type 'exit' to quit): ")
        
        if question.lower() == "exit":
            break

        # next_prompt = question
        # max_turns = 1
        # i = 0
        if len(question) > 0:
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


# [
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "14",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "startupInvestments",
#         "type": "expenditure",
#         "rate": null,
#         "quantity": "59",
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "44",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "startupInvestments",
#         "type": "fund",
#         "rate": null,
#         "quantity": null,
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "10",
#         "unit": null,
#         "frequency": null,
#         "period": "38",
#         "category": "interests-taxes",
#         "type": "loan",
#         "rate": "1",
#         "quantity": null,
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "34",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "fixedCosts",
#         "type": "lease",
#         "rate": null,
#         "quantity": null,
#         "time": {
#             "timerate": "perHour",
#             "perhour": "24",
#             "perday": "7",
#             "perweek": "4",
#             "permonth": "61"
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "2",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "fixedCosts",
#         "type": "utilities",
#         "rate": null,
#         "quantity": null,
#         "time": {
#             "timerate": "perHour",
#             "perhour": "24",
#             "perday": "7",
#             "perweek": "4",
#             "permonth": "19"
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "14",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "fixedCosts",
#         "type": "salariesWages",
#         "rate": null,
#         "quantity": "90",
#         "time": {
#             "timerate": "perHour",
#             "perhour": "24",
#             "perday": "4",
#             "perweek": "4",
#             "permonth": "11"
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "35",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "fixedCosts",
#         "type": "insurance",
#         "rate": null,
#         "quantity": null,
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": null,
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "interests-taxes",
#         "type": "taxes",
#         "rate": "40",
#         "quantity": null,
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "14",
#         "unit": "Sample Text",
#         "frequency": null,
#         "period": null,
#         "category": "variableCosts",
#         "type": "rawMaterials",
#         "rate": null,
#         "quantity": "29",
#         "time": {
#             "timerate": "perDay",
#             "perhour": null,
#             "perday": "7",
#             "perweek": "4",
#             "permonth": "81"
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "97",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "variableCosts",
#         "type": "packaging",
#         "rate": null,
#         "quantity": "26",
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "21",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "variableCosts",
#         "type": "shippingTransportation",
#         "rate": null,
#         "quantity": null,
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "23",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "variableCosts",
#         "type": "marketingAdvertising",
#         "rate": null,
#         "quantity": null,
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "48",
#         "unit": null,
#         "frequency": "hourly",
#         "period": null,
#         "category": "revenues",
#         "type": "productSales",
#         "rate": null,
#         "quantity": "56",
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": null,
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "revenues",
#         "type": "serviceFees",
#         "rate": "42",
#         "quantity": null,
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": null,
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "revenues",
#         "type": "commissions",
#         "rate": "97",
#         "quantity": null,
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "33",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "revenues",
#         "type": "licensingFees",
#         "rate": null,
#         "quantity": "71",
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     },
#     {
#         "name": "Sample Text",
#         "detail": "Sample Text",
#         "amount": "57",
#         "unit": null,
#         "frequency": null,
#         "period": null,
#         "category": "revenues",
#         "type": "royalties",
#         "rate": "9",
#         "quantity": "95",
#         "time": {
#             "timerate": null,
#             "perhour": null,
#             "perday": null,
#             "perweek": null,
#             "permonth": null
#         }
#     }
# ]


# A bakery took out a £65,000 loan at an interest rate of 8.5% over 3 years to purchase essential equipment. Additional funds totaling £22,000 were invested in a commercial oven, dough divider, and a proofer. Monthly overhead costs include £3,000 for rent, £550 for electricity, £5,200 for three employees’ wages, a contractor is paid £20 per hour, 8 hours a day, 4 days a week, 4 weeks a month, and £2,500 for a supervisor’s salary. Daily operational expenses consist of £450 for flour, £15 for salt, £80 for yeast, and £180 for packaging materials. The bakery produces 720 loaves of bread daily, selling each for £2.15. Additionally, the bakery sells 120 pastries daily at £1.50 each.

# **Example Question:**
# A bakery took out a £65,000 loan at an interest rate of 8.5% over 3 years to purchase essential equipment. Additional funds totaling £22,000 were invested in a commercial oven, dough divider, and a proofer. Monthly overhead costs include £3,000 for rent, £550 for electricity, £5,200 for three employees’ wages, a contractor is paid £20 per hour, 8 hours per day, 4 days per week, 4 weeks per month, and £2,500 for a supervisor’s salary. Daily operational expenses consist of £450 for flour, £15 for salt, £80 for yeast, and £180 for packaging materials. The bakery produces 720 loaves of bread daily, selling each for £2.15. Additionally, the bakery sells 120 pastries daily at £1.50 each. Plus 20 scorns are produced hourly, 6 hours per day, 3 days per week and 2 weeks per month selling at £0.85 each.

# **Example Extracted Data:**
# ```json
#     "Startup Investments":[
#         {
#             "category":"startupInvestments",
#             "type":"loan",
#             "name":"Business Loan",
#             "detail":"£65,000 loan for purchasing equipment",
#             "amount":65000,
#             "currency":"GBP",
#             "interest_rate":8.5,
#             "term_years":3
#         },
#         {
#             "category":"startupInvestments",
#             "type":"otherInvestment",
#             "name":"Commercial Equipment",
#             "detail":"Commercial oven, dough divider, and proofer",
#             "amount":22000,
#             "currency":"GBP"
#         }
#     ],
#     "Fixed Costs":[
#         {
#             "category":"fixedCosts",
#             "type":"rent",
#             "name":"Rent",
#             "detail":"Monthly rent for the bakery premises",
#             "amount_per_unit":3000,
#             "unit":"GBP",
#             "billing_frequency":"monthly"
#         },
#         {
#             "category":"fixedCosts",
#             "type":"utilities",
#             "name":"Electricity",
#             "detail":"Monthly electricity bill",
#             "amount_per_unit":550,
#             "unit":"GBP",
#             "billing_frequency":"monthly"
#         },
#         {
#             "category":"fixedCosts",
#             "type":"wages",
#             "name":"Employee Wages",
#             "detail":"Monthly wages for three employees",
#             "amount_per_unit":5200,
#             "unit":"GBP",
#             "billing_frequency":"monthly"
#         },
#         {
#             "category":"fixedCosts",
#             "type":"otherFixedCost",
#             "name":"Contractor Labor",
#             "detail":"Hourly labor cost for a contractor",
#             "amount_per_unit":20,
#             "unit":"GBP",
#             "time_rate":"hourly",
#             "perHour": 8,
#             "perDay": 4,
#             "perWeek": 4,
#             "perMonth": 1,
#         },
#         {
#             "category":"fixedCosts",
#             "type":"otherFixedCost",
#             "name":"Supervisor Salary",
#             "detail":"Monthly salary for the supervisor",
#             "amount_per_unit":2500,
#             "unit":"GBP",
#             "billing_frequency":"monthly"
#         }
#     ],
#     "Variable Costs":[
#         {
#             "category":"variableCosts",
#             "type":"rawMaterials",
#             "name":"Flour",
#             "detail":"Daily flour cost for bread production",
#             "amount_per_unit":450,
#             "unit":"GBP",
#             "billing_frequency":"daily"
#         },
#         {
#             "category":"variableCosts",
#             "type":"otherVariableCost",
#             "name":"Salt",
#             "detail":"Daily salt cost for bread production",
#             "amount_per_unit":15,
#             "unit":"GBP",
#             "billing_frequency":"daily"
#         },
#         {
#             "category":"variableCosts",
#             "type":"otherVariableCost",
#             "name":"Yeast",
#             "detail":"Daily yeast cost for bread production",
#             "amount_per_unit":80,
#             "unit":"GBP",
#             "billing_frequency":"daily"
#         },
#         {
#             "category":"variableCosts",
#             "type":"otherVariableCost",
#             "name":"Packaging Materials",
#             "detail":"Daily packaging materials cost for bread production",
#             "amount_per_unit":180,
#             "unit":"GBP",
#             "billing_frequency":"daily"
#         }
#     ],
#     "Revenue":[
#         {
#             "category":"revenues",
#             "type":"unitSales",
#             "name":"Bread Sales",
#             "detail":"Daily bread sales revenue",
#             "amount_per_unit":2.15,
#         "currency":"GBP",
#         "quantity": 720,
#             "unit":"scorn",
#             "time_rate":"daily"
#         },
#         {
#             "category":"revenues",
#             "type":"unitSales",
#             "name":"Pastry Sales",
#             "detail":"Daily pastry sales revenue",
#             "amount_per_unit": 1.50,
#         "currency":"GBP",
#         "quantity": 120,
#             "unit":"pastry",
#             "time_rate":"daily"
#         },
#         {
#             "category":"revenues",
#             "type":"otherSales",
#             "name":"Scorns",
#             "detail":"Scorns sales revenue",
#             "amount_per_unit":0.85,
#         "currency":"GBP",
#             "unit":"scorn",
#         "quantity": 20,
#             "time_rate":"hourly",
#             "perHour": 6,
#             "perDay": 3,
#             "perWeek": 2,
#             "perMonth": 1,
#         }
#     ]
# ```

# System Prompt #1

# This hard-coded prompt is simply an example JSON, to explain to the model how to parse the structure.

#  ### Example Application:
#     A bakery took out a £65,000 loan at an interest rate of 8.5% over 3 years to purchase essential equipment. Additional funds totaling £22,000 were invested in a commercial oven, dough divider, and a proofer. Monthly overhead costs include £3,000 for rent, £550 for electricity, £5,200 for three employees’ wages, a contractor is paid £20 per hour, 8 hours per day, 4 days per week, 4 weeks per month, and £2,500 for a supervisor’s salary. Daily operational expenses consist of £450 for flour, £15 for salt, £80 for yeast, and £180 for packaging materials. The bakery produces 720 loaves of bread daily, selling each for £2.15. Additionally, the bakery sells 120 pastries daily at £1.50 each. Plus, 40 scones are produced hourly, 6 hours per day, 3 days per week and 2 weeks per month, selling at £0.85 each.

#     ```json
#     {
#        "startupInvestments":[
#           {
#              "category":"startupInvestments",
#              "type":"loan",
#              "name":"Business Loan",
#              "detail":"£65,000 loan with an interest rate of 8.5% over 3 years.",
#              "amount":65000,
#              "currency":"GBP"
#           },
#           {
#              "category":"startupInvestments",
#              "type":"equipment",
#              "name":"Commercial Oven",
#              "detail":"£12,000 investment.",
#              "amount":12000,
#              "currency":"GBP"
#           },
#           {
#              "category":"startupInvestments",
#              "type":"equipment",
#              "name":"Dough Divider",
#              "detail":"£5,000 investment.",
#              "amount":5000,
#              "currency":"GBP"
#           },
#           {
#              "category":"startupInvestments",
#              "type":"equipment",
#              "name":"Proofer",
#              "detail":"£5,000 investment.",
#              "amount":5000,
#              "currency":"GBP"
#           }
#        ],
#        "fixedCosts":[
#           {
#              "category":"fixedCosts",
#              "type":"rent",
#              "name":"Monthly Rent",
#              "detail":"£3,000 per month.",
#              "amount_per_unit":3000,
#              "time_durations":[
#                 {
#                    "time_unit":"month",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"fixedCosts",
#              "type":"utilities",
#              "name":"Electricity",
#              "detail":"£550 per month.",
#              "amount_per_unit":550,
#              "time_durations":[
#                 {
#                    "time_unit":"month",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"fixedCosts",
#              "type":"wages",
#              "name":"Employee Salaries",
#              "detail":"£5,200 per month for three employees.",
#              "amount_per_unit":5200,
#              "time_durations":[
#                 {
#                    "time_unit":"month",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"fixedCosts",
#              "type":"wages",
#              "name":"Contractor",
#              "detail":"£20 per hour, 8 hours per day, 4 days per week, 4 weeks per month.",
#             "amount_per_unit": 20,
#              "rate_per_unit":20,
#              "time_durations":[
#                 {
#                    "time_unit":"hour",
#                    "duration":8
#                 },
#                 {
#                    "time_unit":"day",
#                    "duration":4
#                 },
#                 {
#                    "time_unit":"week",
#                    "duration":4
#                 }
#              ]
#           },
#           {
#              "category":"fixedCosts",
#              "type":"wages",
#              "name":"Supervisor Salary",
#              "detail":"£2,500 per month.",
#              "amount_per_unit":2500,
#              "time_durations":[
#                 {
#                    "time_unit":"month",
#                    "duration":1
#                 }
#              ]
#           }
#        ],
#        "variableCosts":[
#           {
#              "category":"variableCosts",
#              "type":"ingredients",
#              "name":"Flour",
#              "detail":"£450 per day.",
#              "amount_per_unit":450,
#              "time_durations":[
#                 {
#                    "time_unit":"day",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"variableCosts",
#              "type":"ingredients",
#              "name":"Salt",
#              "detail":"£15 per day.",
#              "amount_per_unit":15,
#              "time_durations":[
#                 {
#                    "time_unit":"day",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"variableCosts",
#              "type":"ingredients",
#              "name":"Yeast",
#              "detail":"£80 per day.",
#              "amount_per_unit":80,
#              "time_durations":[
#                 {
#                    "time_unit":"day",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"variableCosts",
#              "type":"ingredients",
#              "name":"Packaging Materials",
#              "detail":"£180 per day.",
#              "amount_per_unit":180,
#              "time_durations":[
#                 {
#                    "time_unit":"day",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"variableCosts",
#              "type":"ingredients",
#              "name":"Scones Ingredients",
#              "detail":"£0.85 per scones, 40 scones are produced hourly.",
#              "rate_per_unit":0.85,
#              "time_durations":[
#                 {
#                    "time_unit":"hour",
#                    "duration":1
#                 }
#              ]
#           }
#        ],
#        "revenue":[
#           {
#              "category":"revenue",
#              "type":"sales",
#              "name":"Bread Sales",
#              "detail":"720 loaves daily at £2.15 each.",
#              "rate_per_unit":2.15,
#              "time_durations":[
#                 {
#                    "time_unit":"day",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"revenue",
#              "type":"sales",
#              "name":"Pastry Sales",
#              "detail":"120 pastries daily at £1.50 each.",
#              "rate_per_unit":1.5,
#              "time_durations":[
#                 {
#                    "time_unit":"day",
#                    "duration":1
#                 }
#              ]
#           },
#           {
#              "category":"revenue",
#              "type":"sales",
#              "name":"Scone Sales",
#              "detail":"40 scones are produced hourly at £0.85 each.",
#             "amount_per_unit": 0.85,
#              "rate_per_unit":40,
#             "time_durations": [
#             {
#             "time_unit": "hour",
#             "duration": 6
#             },
#             {
#             "time_unit": "day",
#             "duration": 3
#             },
#             {
#             "time_unit": "week",
#             "duration": 2
#             }
#         ],
#           }
#        ]
#     }
#     ```


