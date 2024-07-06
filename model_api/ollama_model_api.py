import requests
import json
from .base_model_api import BaseModelAPI

class OllamaAPI(BaseModelAPI):
    def __init__(self, model, prompt_modification, temperature=0):
        self.model = model
        self.prompt_modification = prompt_modification
        self.model_endpoint = 'http://localhost:11434/api/generate'
        self.headers = {"Content-Type": "application/json"}
        self.temperature = temperature

    def run_query(self, prompt):
        payload = {
            "model": self.model,
            "format": "json",
            "prompt": prompt,
            "system": self.prompt_modification,
            "stream": False,
            "temperature": self.temperature,
        }

        try:
            response = requests.post(self.model_endpoint, headers=self.headers, data=json.dumps(payload))
            response_dict = response.json()
            return response_dict['response']
        except requests.RequestException as e:
            return {"error": f"Error invoking the model: {str(e)}"}