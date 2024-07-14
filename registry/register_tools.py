import ast
import os
import sys

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
parent_dir = os.path.join(parent_directory, "registry")
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from .ai_assistants_registry import AiAssistantsRegistry

def register_function(registry, file_path):
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
                            elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)
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

def get_functions_list(registry, assistant_folder_path, excluded_files=[]):
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
                register_function(registry, file_path)


def create_registry():
    # Create an instance of the registry
    registry = AiAssistantsRegistry()
    folder_path = os.path.join(parent_directory, "ai_assistants")
    get_functions_list(registry, folder_path)

    return registry
