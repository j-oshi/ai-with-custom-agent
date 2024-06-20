import unittest
from unittest.mock import patch, Mock
import json
import requests
import os
import sys

parent_dir = os.path.abspath('..')
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from model_api.ollama_model_api import OllamaAPI

class TestOllamaAPI(unittest.TestCase):
    def setUp(self):
        self.model = "test-model"
        self.api = OllamaAPI(self.model)
        self.prompt = "What is the largest state in Nigeria?"

    @patch('requests.post')
    def test_chat_successful_response(self, mock_post):
        # Define the mock response data
        mock_response_data = {'response': 'The largest state in Nigeria is Niger State.'}
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_post.return_value = mock_response

        # Call the chat method
        response = self.api.chat(self.prompt)

        # Assert the response
        self.assertEqual(response, mock_response_data['response'])
        mock_post.assert_called_once_with(
            self.api.model_endpoint,
            headers=self.api.headers,
            data=json.dumps({
                "model": self.api.model,
                "format": "json",
                "prompt": self.prompt,
                "stream": False
            })
        )

    @patch('requests.post')
    def test_chat_request_exception(self, mock_post):
        # Define the exception to be raised by the mock
        mock_post.side_effect = requests.RequestException("Network error")

        # Call the chat method
        response = self.api.chat(self.prompt)

        # Assert the response
        self.assertEqual(response, {"error": "Error invoking the model: Network error"})

if __name__ == '__main__':
    unittest.main()