""" ### Task: Extract and Categorize Data Based on Framework

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

    # Example
    A bakery took out a £65,000 loan at an interest rate of 8.5% over 3 years to purchase essential equipment. Additional funds totaling £22,000 were invested in a commercial oven, dough divider, and a proofer. Monthly overhead costs include £3,000 for rent, £550 for electricity, £5,200 for three employees’ wages, a contractor is paid £20 per hour, 8 hours per day, 4 days per week, 4 weeks per month, and £2,500 for a supervisor’s salary. Daily operational expenses consist of £450 for flour, £15 for salt, £80 for yeast, and £180 for packaging materials. The bakery produces 720 loaves of bread daily, selling each for £2.15. Additionally, the bakery sells 120 pastries daily at £1.50 each. Plus 40 scorns are produced hourly, 6 hours per day, 3 days per week and 2 weeks per month selling at £0.85 each.

    #### Example 1: Contractor Payment
    ```json
    {
    "category": "variableCosts",
    "type": "labor",
    "name": "Contractor Payment",
    "detail": "Hourly payment for contractor services",
    "amount": null,
    "quantity": null,
    "unit": "hour",
    "unit_info": "Labor time",
    "amount_per_unit": 20,
    "interest_rate": null,
    "term_years": null,
    "currency": "GBP",
    "time_durations": [
        {
        "time_unit": "hour",
        "duration": 8
        },
        {
        "time_unit": "day",
        "duration": 4
        },
        {
        "time_unit": "week",
        "duration": 4
        }
    ],
    "rate_per_unit": 20
    }
    ```

    #### Example 2: Scone Production
    ```json
    {
    "category": "revenue",
    "type": "productSales",
    "name": "Scone Sales",
    "detail": "Production and sale of scones",
    "amount": null,
    "quantity": 40,
    "unit": "scone",
    "unit_info": "Production rate",
    "amount_per_unit": 0.85,
    "interest_rate": null,
    "term_years": null,
    "currency": "GBP",
    "time_durations": [
        {
        "time_unit": "hour",
        "duration": 6
        },
        {
        "time_unit": "day",
        "duration": 3
        },
        {
        "time_unit": "week",
        "duration": 2
        },
    ],
    "rate_per_unit": 40
    }
    ```

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
