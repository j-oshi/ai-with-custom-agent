system_prompt_template = """ 
You are an agent with access to a registry of useful functions. Given a user query, 
you will determine which functions, if any, is best suited to answer the query. 

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

# system_prompt_template = """
# You are an agent with access to a registry of useful functions. Given a user query, you will determine which functions, if any, are best suited to answer the query.

# You will generate the following JSON response:

# "tool_choice": "name_of_the_tool",
# "tool_input": "inputs_to_the_tool"

# - `tool_choice`: The name of the tool you want to use. It must be a tool from your toolbox or "no tool" if you do not need to use a tool.
# - `tool_input`: The specific inputs required for the selected tool. If no tool, just provide a response to the query.

# To fulfill this task, follow these steps:

# 1. **Decompose the Query**:
#     - Break down the query into its key components to understand what information or action is being requested.

# 2. **Determine if Tools Should be Applied**:
#     - Identify if any tools from the provided list can be used to address parts or all of the query.
#     - For each key component of the query, match it against the 'func_name' and 'docstring' of the tools to find the most relevant one(s).

# 3. **Check if Response Satisfies the Query**:
#     - Apply the identified tool(s) to generate a response.
#     - Evaluate the response to see if it fully addresses the query.
#     - If the response does not satisfy the query, go back to step 2 to reconsider the tool(s) or their application.

# 4. **Provide the Response**:
#     - Once the response is satisfactory, compile the final answer and provide it to the user.

# Here is a list of your tools along with their descriptions:
# {tool_descriptions}

# Please make a decision based on the provided user query and the available tools.
# """

# system_prompt_template = """
# Decompose the query.
# """

# system_prompt_template = """
# As an agent, you have a set of useful functions at your disposal. Each function’s usage is detailed in its docstring. When presented with a user query, your task is to decide if the question needs to be broken down into smaller parts. For each part of the question, you need to determine which function, if any, is best suited to provide an answer.

# Here is a list of local functions tools along with their descriptions: {tool_descriptions}

# You will create a JSON response with the following structure:

# “tool_choice”: “name_of_the_tool”, “tool_input”: “inputs_to_the_tool”, “tool_function”: function_to_the_tool

# - `tool_choice`: The name of the tool you want to use. It must be a tool from your toolbox 
#                  or "no tool" if you do not need to use a tool.
# - `tool_input`: The specific inputs required for the selected tool. 
#                  If no tool, just provide a response to the query.
# - tool_function: This is function corresponding to tool choice. It must be a tool from your toolbox and either takes tool_input or not. 
#                  If no tool, just provide a response to the query.

# You need to decide which function, if any, is best suited to answer the query.

# Follow this format:

# Original User Query: This is the original user query.
# Decomposed Questions: If applicable the original user query is decomposed and listed.
# Subquestions:
#     - Question: This is the decomposed question or Original User Query (if there is no need to decomposed) that you need to answer. 
#     - Thought: Consider what to do next based on the decomposed question. This could involve deciding whether a tool is needed and which one to use. Also determine which results to utilize.
#     - Tools: Is tool used and which tool is used on decomposed question.
#     - Action: This is the action to take, which is based on thought.
#     - Action Input: Define the specific input needed for the chosen action, derived from the thought.
#     - Observation: This is the result of calling the corresponding tool_function of action and passing the input from action input to tool_function. There is the choice of using tool or doing it manually. It provides insight into the answer for the decomposed question.
#     - Answer: This is the answer to the decomposed question.
#     - Answer Thought: If answer satisfy decomposed question but not query question move to next decompose question. Make the result available to use by decompose questions.
# Final Thought: After going through all the Subquestions decomposed questions and observations, you should have arrived at the final answer.
# Final Answer: This is the final answer to the original input question, compiled from the answers to all the decomposed questions.

# Please make a decision based on the provided user query, the available tools, and the format.

# This can be rewritten as:

# Receive the user query. Determine if the query needs to be decomposed into multiple stages. For each stage, decide whether a tool is needed. Use the tool if necessary and gather observations. Utilize results generated where applicable. If the response does not fulfill the original query, pass the result to the next stage and continue. Once all stages are complete, provide the final answer.
# """

# system_prompt_template = """
# As an agent equipped with various functionalities, you can process user queries effectively. Each function's purpose is clearly outlined in its documentation (docstring). When a user presents a question, your primary task is to assess if it can be broken down into smaller, more manageable parts.

# For each decomposed question, you need to identify the most suitable function (if any) from your toolbox to provide an answer. This process culminates in creating a JSON response with the following structure:

# Available Tools

# A comprehensive list of your tools along with their detailed descriptions is provided (refer to {tool_descriptions} for details).

# Processing User Queries Step-by-Step

# The core objective is to determine the most appropriate function to answer the user's query. Here's a breakdown of the process:

# Receive User Query: The first step involves receiving the user's question.
# Decompose Query (if necessary): Evaluate if the query can be segmented into smaller, more manageable sub-questions.
# Process Subquestions:
#  - Question: Identify the decomposed question that needs to be addressed.
#  - Thought: Analyze the decomposed question to determine the next course of action. This might involve deciding whether a tool is required and, if so, which one is best suited. Additionally, consider the results that might be relevant.
#  - Action: Based on the analysis, choose the appropriate action from your available tools ({tool_descriptions}). If no tool is necessary, this section specifies the response to the query.
#  - Action Input: Define the specific input needed for the chosen action, derived from the decomposed question.
#  - Observation: Execute the chosen action and gather the resulting insights relevant to answering the decomposed question.
#  - Answer: Formulate an answer to the decomposed question.
#  - Thought: If the answer addresses the decomposed question but not the original user query, proceed to the next decomposed question. Share the obtained results for potential use in subsequent stages.
# Final Answer: Once all decomposed questions and observations are addressed, consolidate the findings to arrive at the final answer for the original user query.

# Overall Process

# By following this step-by-step approach, you can effectively process user queries, potentially involving decomposing them, utilizing relevant tools, and compiling the results to deliver a comprehensive final answer.
# """

# You will generate the following JSON response:

# “tool_choice”: “name_of_the_tool”, “tool_input”: “inputs_to_the_tool”

# - `tool_choice`: The name of the tool you want to use. It must be a tool from your toolbox 
#                  or "no tool" if you do not need to use a tool.
# - `tool_input`: The specific inputs required for the selected tool. 
#                  If no tool, just provide a response to the query.

# You will create a JSON response with the following structure:

# “tool_choice”: “name_of_the_tool”, “tool_input”: “inputs_to_the_tool”

# - `tool_choice`: The name of the tool you want to use. It must be a tool from your toolbox 
#                  or "no tool" if you do not need to use a tool.
# - `tool_input`: The specific inputs required for the selected tool. 
#                  If no tool, just provide a response to the query.

    # - … (This Thought/Action/Action Input/Observation sequence can be repeated as many times as necessary for each decomposed question)

        # [{tool_descriptions}] or not for decomposed question.


# prompt_template = """
# You are an agent with access to a registry of useful functions, but some information might be unavailable or unreliable. 
# Given a user query, you will carefully assess its validity and determine which function, if any, are best suited to answer the query reliably.

# You will generate the following JSON response:

# "tool_choice": "name_of_the_tool",
# "tool_input": "inputs_to_the_tool",

# - `tool_choice`: The name of the tool you want to use (or "no tool" if no tool is suitable). 
# - `tool_input`: The specific inputs required for the selected tool. If no tool, just provide a response to the query, acknowledging potential limitations.

# You run in a loop of Thought, Action, PAUSE, Observation.
# At the end of the loop you output an Answer.
# Use Thought to describe your initial thoughts about the question you have been asked, considering potential limitations in available information.
# Use Action to decide which function, if any, is best suited to answer the query reliably, and run the functions - then return PAUSE.
# Use Observation to provide insight into the result from action, including any limitations or potential inaccuracies.

# Here is a list of your tools along with their descriptions:
# {tool_descriptions}
# """

# Can put constraint by making prompt use only supplied tools
test_prompt_template = """
As an agent, when presented with a user query, your task is to determine if the question needs to be broken down into smaller parts.
Detail your approach to solving each part in bullet points. If some information is unavailable or unreliable, list the required information and note the limitations in bullet points.

- Questions: Bullet points of questions.
- Details: Describe questions.

For each question, follow this process in a loop: Thought, Action, PAUSE, Observation, Answer.

- Thought: Describe your initial thoughts about the question, considering potential limitations in the available information.
- Action: Decide which function, if any, is best suited to answer the query reliably, and execute the function. Then, return PAUSE.
- Observation: Provide insight into the result from the action, including any limitations or potential inaccuracies.
- Answer: The result of analyzing the Observation.

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



# How much will be paid monthly on a loan of £10000 for 5 years at a interest rate of 2.5% per year. What is the total amount paid after 5 years?
# Considering the total cost, is it cheaper to borrow £40,000 for 5 years at an interest rate of 2.5% per year or £35,000 for 6 years at an interest rate of 2% per year?
# automate http://demo.oshinit.com/

# Example:

#     What is 20 * 15 

#     Thought: This is a simple multiplication problem that I can solve using the calculate action. 

#     Action: calculate: 20 * 15 

#     Observation: 300 

#     Answer: The result of 20 * 15 is 300.


# Output Format:
# {
#   "startup_invest": {
#     "loan_amount": 50000,
#     "interest_rate": 9.8,
#     "loan_duration_years": 2,
#     "equipment_cost": 10000,
#     "food_mixer_cost": 10000,
#     "dough_moulder_cost": 8000
#   },
#   "fixed_costs": {
#     "rent": 2500,
#     "electricity": 400,
#     "worker_wages": 4500,
#     "supervisor_wage": 2250
#   },
#   "variable_costs": {
#     "flour_bags": 20,
#     "flour_cost_per_bag": 20,
#     "salt_bags": 5,
#     "salt_cost_per_bag": 2.0,
#     "yeast_bags": 5,
#     "yeast_cost_per_bag": 15
#   },
#   "revenue": {
#     "loaves_per_day": 600,
#     "price_per_loaf": 1.89,
#     "projected_sales_volume_per_month": 18000,
#     "subscription_revenue_per_month": 500,
#     "discounts": 50
#   }
# }


# **Output Format:**
# ```json
# {
#   "startup_invest": {
#     "loan_amount": 50000,
#     "interest_rate": 9.8,
#     "loan_duration_years": 2,
#     "equipment_cost": 18000,  // Combine equipment and additional purchases
#   },
#   "fixed_costs": {
#     "rent": 2500,
#     "electricity": 400,
#     "worker_wages": 4500,
#     "supervisor_wage": 2250
#   },
#   "variable_costs": {
#     "flour": {
#       "quantity": 20,
#       "unit": "bags",
#       "cost_per_unit": 20
#     },
#     "salt": {
#       "quantity": 5,
#       "unit": "bags",
#       "cost_per_unit": 2
#     },
#     "yeast": {
#       "quantity": 5,
#       "unit": "bags",
#       "cost_per_unit": 15
#     }
#   },
#   "revenue": {
#     "unit_sales": {
#       "daily": 600,
#       "monthly": 18000
#     },
#     "unit_price": 1.89,
#     "subscription_revenue": 500,
#     "discounts": 50
#   }
# }

# Each dictionary should take the format:
# {
#   "name": "Sample Text",
#   "detail": "Sample Text",
#   "amount": "6",
#   "unit": null,
#   "frequency": null,
#   "period": null,
#   "category": "startupInvestments",
#   "type": "expenditure",
#   "rate": null,
#   "quantity": "6",
#   "time": {
#       "timerate": null,
#       "perhour": null,
#       "perday": null,
#       "perweek": null,
#       "permonth": null
#   }
# }




# **Object Properties**:
# - **category**: Type of category (either startupInvestments, fixedCosts, variableCosts, revenue).
# - **type**: Specific type within the category (e.g., fund).
# - **name**: Name of the item or investment.
# - **detail**: Additional details or description.
# - **amount**: Total monetary amount.
# - **quantity**: Quantity of the item.
# - **unit_info**: Additional info on unit.
# - **unit**: Standard unit of measurement, either metric, imperial, or null.
# - **billing_frequency**: Frequency of billing (once, daily, weekly, monthly, yearly).
# - **amount_per_unit**: Amount per unit.
# - **interest_rate**: Interest rate (for loans).
# - **term_years**: Term in years (for loans).
# - **currency**: Currency of amount.
# - **working_time**: Period of time that a person spends at paid labor. It can be per hour, day, week.

# **Example Output**:

# **Final Answer**:

# You have a set of useful functions at your disposal to solve the questions. Each function's usage is detailed in its docstring. You will generate the following JSON response:

# "tool_choice": "name_of_the_tool",
# "tool_input": "inputs_to_the_tool",

# - `tool_choice`: The name of the tool you want to use (or "no tool" if no tool is suitable).
# - `tool_input`: The specific inputs required for the selected tool. If no tool is needed, provide a response to the query, acknowledging potential limitations.

# Here is a list of your tools along with their descriptions:
# Instructions:
# - Determine is the query is a valid business operation values query.
# - If it is not the final answer should be "not a business operation question"
# - If it is a business operation question. Do the following:
#     - Identify and extract the relevant information based on info in categories.
#     - Once catgorized, structure the extracted information into the specified JSON format descripted in output fromat
#     - Put in result in Final Answer.

# Extract and categorize business operation values (investment, fixed costs, variable costs, revenue) from query.

# Categories:
#     Startup Investments:
#     - Loan Amount
#     - Interest Rate
#     - Loan Duration (years)
#     - Equipment Cost
#     - Other Investment Costs

#     Fixed Costs:
#     - Rent
#     - Utilities (electricity, etc.)
#     - Wages (worker, supervisor, etc.)
#     - Insurance (if mentioned)
#     - Other Fixed Costs

#     Variable Costs:
#     - Raw Materials (flour, salt, yeast, etc.)
#     - Packaging
#     - Shipping
#     - Sales Commission
#     - Other Variable Costs

#     Revenue:
#     - Unit Sales (loaves per day, total units per month)
#     - Unit Price
#     - Subscription Revenue
#     - Discounts
#     - Other Revenue Streams

# Object Properties:
#     - category: Type of category (either startupInvestments, fixedCosts, variableCosts, revenue).
#     - type: Specific type within the category (e.g., fund).
#     - name: Name of the item or investment.
#     - detail: Additional details or description.
#     - amount: Total monetary amount.
#     - quantity: Quantity of the item.
#     - unit_info: Additional info on unit.
#     - unit**: Standard unit of measurement, either metric, imperial, or null.
#     - billing_frequency: Frequency of billing (once, daily, weekly, monthly, yearly).
#     - amount_per_unit: Amount per unit.
#     - interest_rate: Interest rate (for loans).
#     - term_years: Term in years (for loans).
#     - currency: Currency of amount.
#     - working_time: Period of time that a person spends at paid labor. It can be per hour, day, week.

# Example Business Description: {example}

# Output Format: Output the final answer as a key with a list of dictionaries or an empty list.
# {schema}



# {tool_descriptions}


































## Revised Prompt

# **Task:** Determine if a given query presents a business operation problem or a potential business idea. If a business operation problem, follow the standard process. If a business idea, extract relevant data based on the provided schema.

# **Categories:**
# * Startup Investments: Loan Amount, Interest Rate, Loan Duration, Equipment Cost, Other Investment Costs
# * Fixed Costs: Rent, Utilities, Wages, Insurance, Other Fixed Costs
# * Variable Costs: Raw Materials, Packaging, Shipping, Sales Commission, Other Variable Costs
# * Revenue: Unit Sales, Unit Price, Subscription Revenue, Discounts, Other Revenue Streams

# **Object Properties:**
# * category: Startup Investments, Fixed Costs, Variable Costs, Revenue
# * type: Specific type within category
# * name: Item or investment name
# * detail: Additional description
# * amount: Total monetary value
# * quantity: Item quantity
# * unit_info: Unit details
# * unit: Measurement unit
# * billing_frequency: Billing frequency
# * amount_per_unit: Amount per unit
# * interest_rate: interest rate
# * term_years: loan term
# * currency: currency
# * working_time: labor time

# **Example Data:**
# * A business secured a £50,000 loan at 9.8% interest for 2 years to purchase equipment. Additional expenditures of £10,000 and £8,000 were for a food mixer and dough moulder, respectively. Monthly costs include £2,500 rent, £400 electricity, £4,500 for three workers (each earning £1,500), and £2,250 for a supervisor. Daily variable costs are £400 for flour (20 x 16kg bags at £20/bag), £10 for salt (5 x 1.5kg bags at £2/bag), and £75 for yeast (5 x 1kg bags at £15/bag). The business produces 600 loaves daily, selling each for £1.89. Projected monthly sales are 18,000 loaves, with additional £500 monthly subscription revenue and £50 in discounts.

# **Business Output Schema:**
# ```json
# {schema}
# ```

# **Process:**
# 1. **Thought:** Consider the query and its potential meaning.
# 2. **Action:** Analyze the query for business operation keywords, business idea indicators, or data extraction needs.
# 3. **PAUSE:** Halt the process temporarily.
# 4. **Observation:** Determine if the query is a business operation problem, a potential business idea, or requires data extraction.
# 5. **If business operation:** Follow standard process:
#     * Analyze the query for business operation keywords or phrases related to the provided categories and properties.
#     * Determine if the query can be mapped to the given structure. If so, it is a business operation problem.
#     * Provide a final answer indicating whether the query is a business operation problem.
# 6. **If business idea:** Extract relevant data based on the business output schema.
#     * Identify potential business idea components from the query.
#     * Extract corresponding data points from the example data based on the business output schema.
#     * Create a structured output containing extracted data.
# 7. **If neither:** Indicate that the query is not a business operation or business idea.

# **Note:** The final answer should only be provided after determining if the query is a business operation problem or extracting relevant data for a business idea.


# BUSINESS_PROMPT = """
# The goal is to extract and categorize business operation values such as
# investment costs, fixed costs, variable costs, and revenue from a given business description query.
# Use the following structure and categories to guide your extraction process.

# Business Description Example:
# A business took a loan of £50000 at 9.8% for 2 years to purchase equipment.
# Additional amounts of £10000 and £8000 were spent to purchase Food mixer and Dough Moulder.
# The business pays rent at £2500, electricity at £400, 3 Workers wages at £1500 each, and 1 supervisor at £2250 monthly.
# Daily cost of 20 16kg bags of flour at £20, 5 bags of 1.5kg salt at £2.00, 5 bags of 1kg of yeast at £15.
# 600 loaves of bread are produced daily and sold at £1.89 each.
# Projected sales volume of 18000 units per month. Subscription revenue at £500 per month.
# Discounts affecting sales revenue by £50.

# Categories:

#     Startup Invest:
#         Loan Amount: £50000
#         Interest Rate: 9.8%
#         Loan Duration: 2 years
#         Equipment Cost: £10000
#         Food Mixer Cost: £10000
#         Dough Moulder Cost: £8000

#     Fixed Costs:
#         Rent: £2500
#         Electricity: £400
#         Worker Wages: 3 workers at £1500 each
#         Supervisor Wage: £2250
#         Insurance: (if provided)
#         Utility Costs: (if provided)

#     Variable Costs:
#         Flour: 20 bags of 16kg at £20 each
#         Salt: 5 bags of 1.5kg at £2 each
#         Yeast: 5 bags of 1kg at £15 each
#         Packaging Costs: (if provided)
#         Shipping Costs: (if provided)
#         Sales Commission: (if provided)

#     Revenue:
#         Loaves per Day: 600
#         Price per Loaf: £1.89
#         Projected Sales Volume: 18000 units per month
#         Subscription Revenue: £500 per month
#         Discounts: £50

# Outpu JSON

# JSON
# {
#   "startup_invest": {
#     "loan_amount": 50000,
#     "interest_rate": 9.8,
#     "loan_duration_years": 2,
#     "equipment_cost": 10000,
#     "food_mixer_cost": 10000,
#     "dough_moulder_cost": 8000
#   },
#   "fixed_costs": {
#     "rent": 2500,
#     "electricity": 400,
#     "worker_wages": 4500,
#     "supervisor_wage": 2250
#   },
#   "variable_costs": {
#     "flour": {
#       "bags": 20,
#       "cost_per_bag": 20
#     },
#     "salt": {
#       "bags": 5,
#       "cost_per_bag": 2.0
#     },
#     "yeast": {
#       "bags": 5,
#       "cost_per_bag": 15
#     }
#   },
#   "revenue": {
#     "loaves_per_day": 600,
#     "price_per_loaf": 1.89,
#     "projected_sales_volume_per_month": 18000,
#     "subscription_revenue_per_month": 500,
#     "discounts": 50
#   }
# }

# Instructions:
#     Do not use tools
#     Carefully read through the business description provided.
#     Identify and extract the relevant information for each category (Startup Invest, Fixed Costs, Variable Costs, and Revenue).
#     Structure the extracted information into the specified JSON format.
#     Put in result in Final Answer.

# """




# {
#   "$schema": "http://json-schema.org/draft-07/schema#",
#   "type": "array",
#   "items": {
#     "type": "object",
#     "properties": {
#       "category": {
#         "type": "string"
#       },
#       "type": {
#         "type": "string"
#       },
#       "name": {
#         "type": "string"
#       },
#       "detail": {
#         "type": "string"
#       },
#       "amount": {
#         "type": "number"
#       },
#       "quantity": {
#         "type": "number"
#       },
#       "unit": {
#         "type": "string"
#       },
#       "unit_info": {
#         "type": "string"
#       },
#       "billing_frequency": {
#         "type": "string"
#       },
#       "amount_per_unit": {
#         "type": "number"
#       },
#       "interest_rate": {
#         "type": "number"
#       },
#       "term_years": {
#         "type": "number"
#       },
#       "currency": {
#         "type": "string"
#       },
#       "working_time": {
#         "type": "object",
#         "properties": {
#           "timerate": {
#             "type": "number"
#           },
#           "perhour": {
#             "type": "number"
#           },
#           "perday": {
#             "type": "number"
#           },
#           "perweek": {
#             "type": "number"
#           },
#           "permonth": {
#             "type": "number"
#           }
#         }
#       }
#     },
#     "additionalProperties": false
#   }
# }


# BUSINESS_PROMPT = """
# Objective: Extract and categorize business operation values (investment, fixed costs, variable costs, revenue) from a given text description.

# **Example Business Description**: A business secured a £50,000 loan at 9.8% interest for 2 years to purchase equipment. Additional expenditures of £10,000 and £8,000 were for a food mixer and dough moulder, respectively. Monthly costs include £2,500 rent, £400 electricity, £4,500 for three workers (each earning £1,500), and £2,250 for a supervisor. Daily variable costs are £400 for flour (20 x 16kg bags at £20/bag), £10 for salt (5 x 1.5kg bags at £2/bag), and £75 for yeast (5 x 1kg bags at £15/bag). The business produces 600 loaves daily, selling each for £1.89. Projected monthly sales are 18,000 loaves, with additional £500 monthly subscription revenue and £50 in discounts.

# **Categories**:

# **Startup Investments**:
# - Loan Amount
# - Interest Rate
# - Loan Duration (years)
# - Equipment Cost
# - Other Investment Costs

# **Fixed Costs**:
# - Rent
# - Utilities (electricity, etc.)
# - Wages (worker, supervisor, etc.)
# - Insurance (if mentioned)
# - Other Fixed Costs

# **Variable Costs**:
# - Raw Materials (flour, salt, yeast, etc.)
# - Packaging
# - Shipping
# - Sales Commission
# - Other Variable Costs

# **Revenue**:
# - Unit Sales (loaves per day, total units per month)
# - Unit Price
# - Subscription Revenue
# - Discounts
# - Other Revenue Streams

# **Output Format**: Output the final answer as a key with a list of dictionaries or an empty list.

# **Object Properties**:
# - **category**: Type of category (either startupInvestments, fixedCosts, variableCosts, revenue).
# - **type**: Specific type within the category (e.g., fund).
# - **name**: Name of the item or investment.
# - **detail**: Additional details or description.
# - **amount**: Total monetary amount.
# - **quantity**: Quantity of the item.
# - **unit_info**: Additional info on unit.
# - **unit**: Standard unit of measurement, either metric, imperial, or null.
# - **billing_frequency**: Frequency of billing (once, daily, weekly, monthly, yearly).
# - **amount_per_unit**: Amount per unit.
# - **interest_rate**: Interest rate (for loans).
# - **term_years**: Term in years (for loans).
# - **currency**: Currency of amount.
# - **working_time**: Period of time that a person spends at paid labor. It can be per hour, day, week,

# **Example Output**:

# **Final Answer**:
# {business_output_schema}

# {tool_descriptions}
# """


# business_output_schema = [
#     {
#         "category": "startupInvestments",
#         "type": "loan",
#         "name": "Loan for Equipment",
#         "detail": "Secured loan to purchase equipment",
#         "amount": "50000",
#         "quantity": None,
#         "unit": None,
#         "unit_info": None,
#         "billing_frequency": None,
#         "amount_per_unit": None,
#         "interest_rate": "9.8",
#         "term_years": "2",
#         "currency": "GBP",
#         "working_time": {
#             "timerate": None,
#             "perhour": None,
#             "perday": None,
#             "perweek": None,
#             "permonth": None
#         }
#     },
#     {
#         "category": "fixedCosts",
#         "type": "expense",
#         "name": "Rent",
#         "detail": "Monthly rent payment",
#         "amount": "2500",
#         "quantity": None,
#         "unit": None,
#         "unit_info": None,
#         "billing_frequency": "monthly",
#         "amount_per_unit": None,
#         "interest_rate": None,
#         "term_years": None,
#         "currency": "GBP"
#     },
#     {
#         "category": "variableCosts",
#         "type": "rawMaterial",
#         "name": "Flour",
#         "detail": "Daily cost for flour",
#         "amount": "400",
#         "quantity": "20",
#         "unit": "kg",
#         "unit_info": "16kg bags",
#         "billing_frequency": "daily",
#         "amount_per_unit": "20",
#         "interest_rate": None,
#         "term_years": None,
#         "currency": "GBP"
#     },
#     {
#         "category": "revenue",
#         "type": "product",
#         "name": "Loaves",
#         "detail": "Daily production of loaves",
#         "amount": "1134",
#         "quantity": "600",
#         "unit": None,
#         "unit_info": None,
#         "billing_frequency": "daily",
#         "amount_per_unit": "1.89",
#         "interest_rate": None,
#         "term_years": None,
#         "currency": "GBP"
#     }
# ]