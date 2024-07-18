import json
from enum import Enum

class Period(Enum):
    MONTH = ('month', 12)
    YEAR = ('year', 1)

    def __init__(self, tostring, tointeger):
        self.tostring = tostring
        self.tointeger = tointeger

def fixed_rate(principal: float = 0, period: float = 0, interestRate: float = 0, periodType: Period = Period.MONTH.tostring) -> dict:
    """
    Calculate fixed-rate mortgage details based on input arguments.

    Args:
        principal (float): Loan amount.
        period (float): Duration to pay back principal, expressed in months or years.
        interestRate (float): Interest rate on principal.
        periodType (Period): Specify type of period (month or year). Default is month.

    Returns:
        dict: A dictionary containing:
            - 'interestRate': Interest rate per period at either month or year depends on args periodType.
            - 'periodPayment': Payment. Frequency of payment at either month or year depends on args periodType.
            - 'totalCostOfMortgage': Total cost of the mortgage.
            - 'periodType': Type of payment period either month or year.
    """

    if principal > 0 and period > 0 and interestRate > 0:
        periodInterestRate = interestRate / (100 * periodType.tointeger)
        periodPayment = (principal * (periodInterestRate * ((1 + periodInterestRate) ** period))) / (((1 + periodInterestRate) ** period) - 1)
        totalCostOfMortgage = periodPayment * period
        return {
            'interestRate': periodInterestRate,
            'periodPayment': periodPayment,
            'totalCostOfMortgage': totalCostOfMortgage,
            'periodType': periodType.tostring,
            'period': period
        }
    return {'interestRate': 0, 'periodPayment': 0, 'totalCostOfMortgage': 0, 'periodType': periodType.tostring, "period": period}

def fixed_rate_prompt(input_data):
    """
    Calculate the total amount after fixed-rate interest.

    Parameters:
    input_data (str or dict): A JSON string or dictionary containing the following keys:
        - "principal": The principal amount.
        - "period": The time period ('month' or 'year').
        - "interestRate": The interest rate  ('month' or 'year').
        - "periodType": The type of period ('month' or 'year').
        Example: '{"principal": 5000, "period": 3, "interestRate": 2.5, 'periodType': 'month'}' or {'principal': 6000, 'period': 4.2, 'interestRate': 3.4, 'periodType': 'year'}

    Returns:
    fixed_rate_result (dictionary): A JSON result of the operation containing:
        - "interestRate": The interest rate is the periodic rate  ('month' or 'year').
        - "periodType": Period type value in string form ('month' or 'year').
        - "period": Duration of loan payment.
        - "periodPayment": The periodic payment on loan amount based on period type ('month' or 'year').
        - "totalCostOfMortgage": Total amount paid to payoff loan.
    """
    try:
        if isinstance(input_data, str):
            input_data = input_data.replace("'", "\"").strip().strip("\"")
            input_dict = json.loads(input_data)
        elif isinstance(input_data, dict):
            input_dict = input_data
        else:
            raise ValueError("Invalid input type. Please provide a JSON string or dictionary.")

        principal = input_dict.get("principal", 0)
        period = input_dict.get("period", 0)
        interest_rate = input_dict.get("interestRate", 0)
        period_type_str = input_dict.get("periodType", "month").lower()
        
        period_type = Period.MONTH if period_type_str == "month" else Period.YEAR

        fixed_rate_result = fixed_rate(principal, period, interest_rate, period_type)

        return fixed_rate_result
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return {"error": str(e), "message": "Invalid input format. Please provide a valid JSON string or dictionary."}
    
def fixed_rate_string_formated_prompt(input_data):
    """
    Format the JSON string result of fixed_rate_prompt to sentence string.

    Parameters:
    input_data (str or dict): A JSON string or dictionary containing the following keys:
        - "interestRate": The interest rate is the periodic rate.
        - "periodType": Period type value in string form. It is either month or year.
        - "period": Duration of loan payment.
        - "periodPayment": The periodic payment on loan amount based on period type.
        - "totalCostOfMortgage": Total amount paid to payoff loan.
        Example: '{"principal": 5000, "period": 5, "interestRate": 2.5, "totalCostOfMortgage":  5600, 'periodType': 'year'}' or "{'principal': 6000, 'period': 5, 'interestRate': 3.4, "totalCostOfMortgage":  6600, 'periodType': 'year'}"

    Returns:
    str: The summary of the result.
    """

    try:
        if isinstance(input_data, str):
            input_data = input_data.replace("'", "\"").strip().strip("\"")
            input_dict = json.loads(input_data)
        elif isinstance(input_data, dict):
            input_dict = input_data
        else:
            raise ValueError("Invalid input type. Please provide a JSON string or dictionary.")

        totalCostOfMortgage = input_dict.get("totalCostOfMortgage", 0)
        period = input_dict.get("period", 0)
        interest_rate = input_dict.get("interestRate", 0)
        period_type_str = input_dict.get("periodType").lower()
        periodPayment = input_dict.get("periodPayment", 0)
        
        period_type = Period.MONTH.tostring if period_type_str == "month" else Period.YEAR.tostring

        return f"The total cost of the loan is {totalCostOfMortgage} over {period} {period_type}s. There is a {period_type}ly cost of {periodPayment} and a {period_type}ly interest rate of {interest_rate * 100}%"
        
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": str(e), "message": "Invalid input format. Please provide a valid JSON string."}

__all__ = ['fixed_rate_prompt', "fixed_rate_string_formated_prompt"]

