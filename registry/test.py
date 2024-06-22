# class FunctionRegistry:
#     def __init__(self):
#         self.registry = {}

#     def register_function(self, func_name, docstring, func):
#         """
#         Register a function in the registry.

#         Args:
#             func_name (str): Name of the function.
#             docstring (str): Docstring for the function.
#             func (callable): The actual function.

#         Returns:
#             None
#         """
#         self.registry[func_name] = {'func_name': func_name, 'docstring': docstring, 'function': func}

#     def call_function(self, func_name, *args, **kwargs):
#         """
#         Call a registered function by name.

#         Args:
#             func_name (str): Name of the function.
#             *args: Positional arguments to pass to the function.
#             **kwargs: Keyword arguments to pass to the function.

#         Returns:
#             Any: Result of the function call.
#         """
#         if func_name in self.registry:
#             return self.registry[func_name]['function']  # Call the function with provided arguments
#         else:
#             raise ValueError(f"Function '{func_name}' not found in the registry.")

# # Example usage:
# def double(x):
#     return 2 * x

# registry = FunctionRegistry()
# registry.register_function('double', "Doubles the input value", double)

# result = registry.call_function('double', 5)
# print(f"Result of doubling 5: {result}")

# result2 = registry.call_function('double', 1000, 2, 2.5)
# print(f"Result of doubling 1000, 2, and 2.5: {result2}")


import os
import sys

parent_dir = os.path.abspath('.')
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from ai_assistants_registry import registry

def main():
    # List available functions
    functions = registry.list_functions()
    print(functions)
    func_name = functions[0]['func_name']

    print(registry.execute_function(func_name, '{"principal": 5000, "period": 3, "interestRate": 2.5}'))


# # User selection loop
# while True:
#     choice = input("Select a function (or 'q' to quit): ")
#     if choice.lower() == 'q':
#         break

#     # Execute the selected function
#     result = registry.execute_function(choice)
#     if result is not None:
#         print(f"Function '{choice}' returned: {result}")

if __name__ == "__main__":
    main()


