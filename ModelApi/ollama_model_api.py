import requests
import json
from .base_model_api import BaseModelAPI

class OllamaAPI(BaseModelAPI):
    def __init__(self, model):
        self.model = model
        self.model_endpoint = 'http://localhost:11434/api/generate'
        self.headers = {"Content-Type": "application/json"}

    def chat(self, prompt):
        payload = {
            "model": self.model,
            "format": "json",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.model_endpoint, headers=self.headers, data=json.dumps(payload))
            response_dict = response.json()
            print(response)
            return response_dict['response']
        except requests.RequestException as e:
            return {"error": f"Error invoking the model: {str(e)}"}