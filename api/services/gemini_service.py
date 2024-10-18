# api/services/gemini_service.py

import requests

class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://gemini-api-url.com"

    def get_health_recommendation(self, symptoms):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        data = {'symptoms': symptoms}
        response = requests.post(f'{self.base_url}/diagnose', json=data, headers=headers)
        return response.json()
