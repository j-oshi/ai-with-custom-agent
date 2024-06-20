import unittest
import os
import sys

parent_dir = os.path.abspath('..')
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
from ai_assistants.assistants.financial.fixed_rate import fixed_rate_prompt

class TestFixedRatePrompt(unittest.TestCase):

    def test_valid_input(self):
        input_str = '{"principal": 5000, "period": 3, "interestRate": 2.5, "periodType": "year"}'
        expected_output = {
            'interestRate': 0.025,
            'periodPayment': 1750.6858362121595,
            'totalCostOfMortgage': 5252.057508636479, 
            'period': 'year'
        }
        result = fixed_rate_prompt(input_str)
        self.assertAlmostEqual(
            result['interestRate'], expected_output['interestRate'])
        self.assertAlmostEqual(
            result['periodPayment'], expected_output['periodPayment'], places=2)
        self.assertAlmostEqual(
            result['totalCostOfMortgage'], expected_output['totalCostOfMortgage'], places=2)
        # self.assertEqual(result['period'], expected_output['period'])

    # def test_invalid_json(self):
    #     input_str = "{'principal': 5000, 'period': 3, 'interestRate': 2.5, 'periodType': 'year'}"
    #     result = fixed_rate_prompt(input_str)
    #     self.assertEqual(result, ("Expecting ',' delimiter: line 1 column 63 (char 62)",
    #                      "Invalid input format. Please provide a valid JSON string."))

    # def test_missing_key(self):
    #     input_str = '{"principal": 5000, "period": 3}'
    #     expected_output = {
    #         'interestRate': 0,
    #         'periodPayment': 0,
    #         'totalCostOfMortgage': 0,
    #         'period': 'year'
    #     }
    #     result = fixed_rate_prompt(input_str)
    #     self.assertEqual(result, expected_output)

    # def test_zero_values(self):
    #     input_str = '{"principal": 0, "period": 0, "interestRate": 0, "periodType": "year"}'
    #     expected_output = {
    #         'interestRate': 0,
    #         'periodPayment': 0,
    #         'totalCostOfMortgage': 0,
    #         'period': 'year'
    #     }
    #     result = fixed_rate_prompt(input_str)
    #     self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
