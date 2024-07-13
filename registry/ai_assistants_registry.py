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
            "func": node,
        }
    
    def list_functions(self):
      """
      Get a list of registered functions and their docstrings.

      Returns:
        List[dict]: List of dictionaries containing 'func_name' and 'docstring'.
      """

      return [{'func_name': name, 'docstring': info['docstring'], 'func': info['func']} for name, info in self.registry.items()]

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
        