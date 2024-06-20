
from enum import Enum

class Period(Enum):
    MONTH = 'month', 12
    YEAR = 'year', 1

    def __init__(self, tostring, tointeger):
        self.tostring = tostring
        self.tointeger = tointeger

def fixed_rate(principal: int | float = 0, period: int | float = 0, interestRate: int | float = 0, periodType: Period = Period.MONTH) -> dict:
    ''' 
        Calculate interest rate for st period based on arguements.
        
        principal
            Loan in int or float format.
        period
            Duration to pay back principal. Value expressed as months in int or float format
        interestRate
            Interest rate on principal. Value in int or float format.
        periodType
            Specify type of period, annually or monthly. Defualt is monthly. Expressed as Period.MONTH or Period.YEAR to period of fixed rate payment.
        return a dictionary of interestRate, periodPayment, totalCostOfMortgage and period
    '''

    if principal > 0 and period > 0 and interestRate > 0:
        periodInterestRate = interestRate / (100 * periodType.tointeger)
        periodPayment = (principal * (periodInterestRate * ((1 + periodInterestRate) ** period))) / (((1 + periodInterestRate) ** period) - 1)
        totalCostOfMortgage = periodPayment * period
        return {
            'interestRate': periodInterestRate,
            'periodPayment': periodPayment,
            'totalCostOfMortgage': totalCostOfMortgage,
            'period': periodType.tostring
        }
    return { 'interestRate': 0, 'periodPayment': 0, 'totalCostOfMortgage': 0 , 'period': periodType.tostring }