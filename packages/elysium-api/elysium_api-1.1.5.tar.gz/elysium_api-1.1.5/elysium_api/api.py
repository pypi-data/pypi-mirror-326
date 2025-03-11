import requests
from typing import Dict, Any, Optional
from .clients import ClientsAPI
from .plans import PlansAPI
from .messages import MessagesAPI

class ElysiumApi:
    def __init__(self, config: Dict[str, str]):
        self.email = config["email"]
        self.hash = config["hash"]
        self.base_url = config.get("base_url", "https://elysiumx.com.br")
        
        # Inicializa as APIs
        self.clients = ClientsAPI(self)
        self.plans = PlansAPI(self)
        self.messages = MessagesAPI(self)

    def get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "email": self.email,
            "hash": self.hash
        }

    # Métodos para clientes
    def create_client(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.clients.create(data)

    def update_client(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.clients.update(data)

    def list_clients(self, **kwargs) -> Dict[str, Any]:
        return self.clients.list(**kwargs)

    def delete_client(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.clients.delete(data)

    def get_client(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.clients.get(data)

    # Métodos para planos
    def create_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.plans.create(data)

    def update_plan(self, plan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.plans.update(plan_id, data)

    def list_plans(self, **kwargs) -> Dict[str, Any]:
        return self.plans.list(**kwargs)

    # Métodos para mensagens
    def send_message_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.messages.send_all_plan(data)

    def send_single_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.messages.send_single(data)

    def _handle_error(self, error: Any) -> Dict[str, Any]:
        if hasattr(error, "response"):
            status = error.response.status_code
            data = error.response.json()

            error_messages = {
                400: "Requisição inválida",
                401: "Credenciais inválidas",
                403: "Sem permissão para acessar este recurso",
                404: "Recurso não encontrado",
                409: "Conflito na operação",
                500: "Erro interno do servidor"
            }

            return {
                "status": status,
                "message": data.get("error") or error_messages.get(status, "Erro desconhecido"),
                "details": data.get("details") or data
            }

        if isinstance(error, requests.exceptions.ConnectionError):
            return {
                "status": 503,
                "message": "Servidor indisponível",
                "details": "Não foi possível conectar ao servidor"
            }

        return {
            "status": getattr(error, "status", 500),
            "message": str(error) or "Erro interno na API",
            "details": getattr(error, "code", "Erro desconhecido")
        }