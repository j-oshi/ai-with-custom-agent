import requests
import json
from .base_model_api import BaseModelAPI


class OllamaAPI(BaseModelAPI):
    def __init__(self, model, system="", assistant="", temperature=0, stream=False, raw=False):
        self.model = model
        self.system = system
        self.assistant = assistant
        self.temperature = temperature
        self.stream = stream
        self.raw = raw
        self.messages = []
        self.model_endpoint = 'http://localhost:11434/api/'  # Base endpoint
        self.headers = {"Content-Type": "application/json"}
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def chat(self, message, tools=None):
        """
        Interact with the chat endpoint.

        Args:
            message (str): The user's input message.
            tools (list): Optional. A list of tools/functions to include in the payload.

        Returns:
            str: The assistant's response.
        """
        self.messages.append({"role": "user", "content": message})
        if bool(self.assistant):
            self.messages.append({"role": "assistant", "content": self.assistant})
        result = self._execute_chat(tools)
        return result

    def generate(self, prompt, suffix=""):
        """
        Interact with the generate endpoint.

        Args:
            prompt (str): The input prompt to generate a continuation from.
            suffix (str): Optional. A suffix to append to the generated text.

        Returns:
            str: The generated text.
        """
        result = self._execute_generate(prompt, suffix)
        return result

    def _execute_chat(self, tools=None):
        payload = {
            "model": self.model,
            "messages": self.messages,
            "stream": self.stream,
            "options": {
                "temperature": self.temperature,
            },
            "tools": tools or [],
            "format": "json", 
        }

        try:
            response = requests.post(f"{self.model_endpoint}chat", headers=self.headers, data=json.dumps(payload))
            response_dict = response.json()

            return response_dict['message']['content']
        except requests.RequestException as e:
            return {"error": f"Error invoking the model: {str(e)}"}

    def _execute_generate(self, prompt, suffix):
        payload = {
            "model": self.model,
            "system": self.system,
            "prompt": prompt,
            "suffix": suffix,
            "options": {
                "temperature": self.temperature,
            },
            "stream": self.stream,
            # "raw": self.raw,
        }

        try:
            response = requests.post(f"{self.model_endpoint}generate", headers=self.headers, data=json.dumps(payload))
            response_dict = response.json()
            return response_dict['response']
        except requests.RequestException as e:
            return {"error": f"Error invoking the model: {str(e)}"}

# class OllamaAPI(BaseModelAPI):
#     def __init__(self, model, system="", temperature=0, stream=False, raw=False):
#         self.model = model
#         self.system = system
#         self.temperature = temperature
#         self.stream = stream
#         self.raw = raw
#         self.messages = []
#         self.model_endpoint = 'http://localhost:11434/api/chat'
#         self.headers = {"Content-Type": "application/json"}
#         if self.system:
#             self.messages.append({"role": "system", "content": system})

#     def chat(self, message):
#         self.messages.append({"role": "user", "content": message})
#         result = self.execute()
#         self.messages.append({"role": "assistant", "content": result})
#         return result

#     def execute(self):
#         payload = {
#             "model": self.model,
#             "format": "json",
#             "messages": self.messages,
#             "options": {
#                 "temperature": self.temperature,
#             },
#             "stream": self.stream,
#             "raw": self.raw,
#         }

#         try:
#             response = requests.post(self.model_endpoint, headers=self.headers, data=json.dumps(payload))
#             response_dict = response.json()

#             return response_dict['message']['content']
#         except requests.RequestException as e:
#             return {"error": f"Error invoking the model: {str(e)}"}