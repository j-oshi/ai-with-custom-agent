import requests
import json
import os

from .base_model_api import BaseModelAPI
from utils.config import load_config

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

config_path = os.path.join(os.path.dirname(current_directory), '..', 'config.yaml')

load_config(config_path)

class OpenaiAPI(BaseModelAPI):
    def __init__(self, model):
        self.model = model
        self.model_endpoint = 'https://api.openai.com/v1/chat/completions'
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def chat(self, prompt):
        payload = {
            "model": self.model,
            "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

        response = requests.post(self.model_endpoint, headers=self.headers, data=json.dumps(payload))
        response_json = response.json()

        if 'choices' in response_json:
            return response_json['choices'][0]['message']['content']
        else:
            raise Exception(f"Error in response: {response_json}")
