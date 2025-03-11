import requests
from typing import Dict, Any, Optional

class ClientsAPI:
    def __init__(self, api):
        self.api = api

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.api.base_url}/api/external/clients/create",
                json=data,
                headers=self.api.get_headers()
            )
            return response.json()
        except Exception as error:
            raise self.api._handle_error(error)

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.put(
                f"{self.api.base_url}/api/external/clients/update?identificador_tipo={data['identificador_tipo']}&identificador_valor={data['identificador_valor']}",
                json=data,
                headers=self.api.get_headers()
            )
            return response.json()
        except Exception as error:
            raise self.api._handle_error(error)

    def list(self, status: Optional[str] = None, search: Optional[str] = None, 
             page: int = 1, limit: int = 10) -> Dict[str, Any]:
        try:
            params = {}
            if status:
                params["status"] = status
            if search:
                params["search"] = search
            if page:
                params["page"] = page
            if limit:
                params["limit"] = limit

            response = requests.get(
                f"{self.api.base_url}/api/external/clients/list",
                params=params,
                headers=self.api.get_headers()
            )
            return response.json()
        except Exception as error:
            raise self.api._handle_error(error)