import requests
from typing import Dict, Any, Optional

class PlansAPI:
    def __init__(self, api):
        self.api = api

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.api.base_url}/api/external/plans/create",
                json=data,
                headers=self.api.get_headers()
            )
            return response.json()
        except Exception as error:
            raise self.api._handle_error(error)

    def update(self, plan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data["plano_id"] = plan_id
            response = requests.put(
                f"{self.api.base_url}/api/external/plans/update",
                json=data,
                headers=self.api.get_headers()
            )
            return response.json()
        except Exception as error:
            raise self.api._handle_error(error)

    def list(self, search: Optional[str] = None, 
             page: int = 1, limit: int = 10) -> Dict[str, Any]:
        try:
            params = {}
            if search:
                params["search"] = search
            if page:
                params["page"] = page
            if limit:
                params["limit"] = limit

            response = requests.get(
                f"{self.api.base_url}/api/external/plans/list",
                params=params,
                headers=self.api.get_headers()
            )
            return response.json()
        except Exception as error:
            raise self.api._handle_error(error)