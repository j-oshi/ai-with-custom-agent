import json
from enum import Enum

class Period(Enum):
    MONTH = ('month', 12)
    YEAR = ('year', 1)

    def __init__(self, tostring, tointeger):
        self.tostring = tostring
        self.tointeger = tointeger

def fixed_rate(principal: float = 0, period: float = 0, interestRate: float = 0, periodType: Period = Period.MONTH) -> dict:
    """
    Calculate fixed-rate mortgage details based on input arguments.

    Args:
        principal (float): Loan amount.
        period (float): Duration to pay back principal, expressed in months or years.
        interestRate (float): Interest rate on principal.
        periodType (Period): Specify type of period (monthly or annually). Default is monthly.

    Returns:
        dict: A dictionary containing:
            - 'interestRate': Interest rate per period.
            - 'periodPayment': Monthly or annual payment amount.
            - 'totalCostOfMortgage': Total cost of the mortgage.
            - 'periodType': Type of payment period (monthly or annually).
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

def fixed_rate_prompt(input_str):
    """
    Calculate the total amount after fixed-rate interest.

    Parameters:
    input_str (str): A JSON string containing the following keys:
        - "principal": The principal amount (initial investment).
        - "period": The time period in years.
        - "interestRate": The annual interest rate (in percentage).
        - "periodType": The type of period ('month' or 'year'). Optional, defaults to 'month'.
        Example: '{"principal": 5000, "period": 3, "interestRate": 2.5}' or "{'principal': 6000, 'period': 4.2, 'interestRate': 3.4, 'periodType': 'year'}"

    Returns:
    fixed_rate_resul (dictionary): A JSOn result of the operation containing:
        - "interestRate": The interest rate is the periodic rate that is monthly if the period type is month, otherwise it is annually.
        - "periodType": Period type value in string form. It is either month or year.
        - "period": Duration of loan payment. Monthly if periodType is month otherwise annually.
        - "periodPayment": The periodic payment on loan amount based on period type. If period type is month, it is a monthly payment otherwise annual payment.
        - "totalCostOfMortgage": Total amount paid to payoff loan. It is based on periodPayment and period.
    str: The formatted result of the operation.
    """
    try:
        input_str_clean = input_str.replace("'", "\"").strip().strip("\"")
        input_dict = json.loads(input_str_clean)
        principal = input_dict.get("principal", 0)
        period = input_dict.get("period", 0)
        interest_rate = input_dict.get("interestRate", 0)
        period_type_str = input_dict.get("periodType", "month").lower()
        
        period_type = Period.MONTH if period_type_str == "month" else Period.YEAR

        fixed_rate_result = fixed_rate(principal, period, interest_rate, period_type)

        return fixed_rate_result
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": str(e), "message": "Invalid input format. Please provide a valid JSON string."}
    
def fixed_rate_string_formated_prompt(input_str):
    """
    Format the result of fixed_rate_prompt to sentence string.

    Parameters:
    input_str (str): A JSON string containing the following keys:
        - "interestRate": The interest rate is the periodic rate that is monthly if the period type is month, otherwise it is annually.
        - "periodType": Period type value in string form. It is either month or year.
        - "period": Duration of loan payment. Monthly if periodType is month otherwise annually.
        - "periodPayment": The periodic payment on loan amount based on period type. If period type is month, it is a monthly payment otherwise annual payment.
        - "totalCostOfMortgage": Total amount paid to payoff loan. It is based on periodPayment and period.
        Example: '{""interestRate": 5000, "period": "month", "interestRate": 2.5, "totalCostOfMortgage"":  5600}' or "{'principal': 6000, 'period': 4.2, 'interestRate': 3.4, 'periodType': 'year'}"

    Returns:
    str: The formatted result of the operation.
    """

    try:
        input_str_clean = input_str.replace("'", "\"").strip().strip("\"")
        input_dict = json.loads(input_str_clean)
        totalCostOfMortgage = input_dict.get("totalCostOfMortgage", 0)
        period = input_dict.get("period", 0)
        interest_rate = input_dict.get("interestRate", 0)
        period_type_str = input_dict.get("periodType", "month").lower()
        periodPayment = input_dict.get("periodPayment", 0)
        
        period_type = Period.MONTH if period_type_str == "month" else Period.YEAR

        return f'The total cost is {totalCostOfMortgage} paid {period_type}ly for a {period_type}ly period of {period}. {periodPayment} is paid {period_type}ly at {interest_rate}% {period_type}ly.'
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": str(e), "message": "Invalid input format. Please provide a valid JSON string."}

__all__ = ['fixed_rate_prompt', "fixed_rate_string_formated_prompt"]

