import ast
import os
import sys

class AiAssistantsRegistry:
    """
    A class to register functions, store details, and provide selection/execution.
    """

    def __init__(self):
        self.registry = {}

    def register(self, name, docstring, node):
        """
        Registers a function by storing its name, docstring, and reference.

        Args:
            func: The function to be registered.

        Returns:
            The original function.
        """

        self.registry[name] = {
            "name": name,
            "docstring": docstring,
            "function": node,
        }
    
    def list_functions(self):
      """
      Get a list of registered functions and their docstrings.

      Returns:
        List[dict]: List of dictionaries containing 'func_name' and 'docstring'.
      """
      return [{'func_name': name, 'docstring': info['docstring']} for name, info in self.registry.items()]

    def select_function(self, name):
        """
        Returns the function object based on the provided name.

        Args:
            name: The name of the registered function.

        Returns:
            The registered function object or None if not found.
        """
        if name in self.registry:
            return self.registry[name]["function"]
        else:
            return None

    def execute_function(self, name, *args, **kwargs):
        """
        Executes the selected function with optional arguments.

        Args:
            name: The name of the registered function.
            *args: Variable positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            The return value of the executed function (if any).
        """
        func = self.select_function(name)
        if func:
            return func(*args, **kwargs)
        else:
            print(f"Function '{name}' not found in registry.")
            return None
        

parent_dir = os.path.abspath("..")
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


# Create an instance of the registry
registry = AiAssistantsRegistry()


def register_function(file_path):
    """
    Extract function names and their docstrings from a given Python file,
    considering only functions listed in the __all__ variable if it exists.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list[dict]: A list of dictionaries, each containing 'func_name', 'docstring', and 'function'.
    """

    with open(file_path, "r") as file:
        file_content = file.read()

    tree = ast.parse(file_content, filename=file_path)

    # Initialize a set to store function names specified in __all__
    all_functions = set()

    # Traverse the AST to find __all__ assignment and function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Check if __all__ is assigned
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    # Extract function names from __all__
                    if isinstance(node.value, ast.List):
                        all_functions.update(
                            elt.s for elt in node.value.elts if isinstance(elt, ast.Str)
                        )

    for node in ast.walk(tree):
      if isinstance(node, ast.FunctionDef):
        node.decorator_list.clear()
        func_name = node.name
        code = compile(tree, func_name, 'exec')
        temp_globals = dict(globals())
        exec(code, temp_globals)
    
        
        # Include the function only if it is in the __all__ or if __all__ is not defined
        if not all_functions or func_name in all_functions:
          docstring = ast.get_docstring(node) or "No docstring available."
          func = temp_globals[func_name]
          registry.register(func_name, docstring, func)

def get_functions_list(assistant_folder_path, excluded_files=[]):
    """
    Get a list of all functions and their docstrings from Python files in the specified directory,
    excluding files in the excluded_files list.

    Args:
        assistant_folder_path (str): Path to the folder containing the assistant files.
        excluded_files (list): List of files to be excluded.

    Returns:
        list[dict]: A list of dictionaries, each containing 'func_name' and 'docstring'.
    """

    # Walk through the directory structure
    for root, dirs, files in os.walk(assistant_folder_path):
        for file in files:
            if file.endswith(".py") and file not in excluded_files:
                file_path = os.path.join(root, file)
                register_function(file_path)

folder_path = os.path.join(parent_dir, "ai_assistants")
get_functions_list(folder_path)
