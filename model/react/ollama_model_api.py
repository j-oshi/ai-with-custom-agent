import requests
import json
from .base_model_api import BaseModelAPI

class OllamaAPI(BaseModelAPI):
    def __init__(self, model, system="", temperature=0):
        self.model = model
        self.system = system
        self.messages = []
        self.model_endpoint = 'http://localhost:11434/api/chat'
        self.headers = {"Content-Type": "application/json"}
        self.temperature = temperature
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        payload = {
            "model": self.model,
            "format": "json",
            "messages": self.messages,
            "options": {
                "temperature": self.temperature,
            },
            "stream": False,
        }

        try:
            response = requests.post(self.model_endpoint, headers=self.headers, data=json.dumps(payload))
            response_dict = response.json()
            print('this is the response')
            print(response_dict)
            return response_dict['message']['content']
        except requests.RequestException as e:
            return {"error": f"Error invoking the model: {str(e)}"}