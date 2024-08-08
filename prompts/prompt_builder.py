import json


class PromptBuilder:
    """Class to build prompts dynamically using schemas and examples."""

    def __init__(self, schema, example, tool_descriptions, prompt_template):
        self.schema = schema
        self.example = example
        self.tool_descriptions = tool_descriptions.list_functions(),
        self.prompt_template = prompt_template

    def build_prompt(self):
        """Constructs the prompt using the provided schema, example, and template."""
        return self.prompt_template.format(
            example=self.example,
            tool_descriptions=self.tool_descriptions,
            schema=json.dumps(self.schema, indent=4)
        )
