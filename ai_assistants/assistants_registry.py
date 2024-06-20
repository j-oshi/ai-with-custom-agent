import os
import ast
import importlib.util

def import_module_from_file(file_path):
    """
    Dynamically import a module from a given file path.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        module: The imported module.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def register_function(file_path):
    """
    Extract function names and their docstrings from a given Python file, 
    considering only functions listed in the __all__ variable if it exists.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list[dict]: A list of dictionaries, each containing 'func_name' and 'docstring'.
    """
    function_list = []

    with open(file_path, 'r') as file:
        file_content = file.read()

    tree = ast.parse(file_content, filename=file_path)

    # Initialize a set to store function names specified in __all__
    all_functions = set()

    # Traverse the AST to find __all__ assignment and function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Check if __all__ is assigned
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == '__all__':
                    # Extract function names from __all__
                    if isinstance(node.value, ast.List):
                        all_functions.update(
                            elt.s for elt in node.value.elts if isinstance(elt, ast.Str)
                        )

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            # Include the function only if it is in the __all__ or if __all__ is not defined
            if not all_functions or func_name in all_functions:
                docstring = ast.get_docstring(node) or "No docstring available."
                function_list.append(
                    {'func_name': func_name, 'docstring': docstring})

    return function_list


def get_functions_list(assistant_folder_path, excluded_files):
    """
    Get a list of all functions and their docstrings from Python files in the specified directory,
    excluding files in the excluded_files list.

    Args:
        assistant_folder_path (str): Path to the folder containing the assistant files.
        excluded_files (list): List of files to be excluded.

    Returns:
        list[dict]: A list of dictionaries, each containing 'func_name' and 'docstring'.
    """
    all_functions = []
    
    # Walk through the directory structure
    for root, dirs, files in os.walk(assistant_folder_path):
        for file in files:
            if file.endswith('.py') and file not in excluded_files:
                file_path = os.path.join(root, file)
                functions = register_function(file_path)
                all_functions.extend(functions)

    return all_functions


