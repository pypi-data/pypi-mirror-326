import requests
from typing import Dict, Any

class MessagesAPI:
    def __init__(self, api):
        self.api = api

    def send_all_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.api.base_url}/api/external/messages/send",
                json=data,
                headers=self.api.get_headers()
            )
            return response.json()
        except Exception as error:
            raise self.api._handle_error(error)

    def send_single(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.api.base_url}/api/external/messages/send-single",
                json=data,
                headers=self.api.get_headers()
            )
            return response.json()
        except Exception as error:
            raise self.api._handle_error(error)