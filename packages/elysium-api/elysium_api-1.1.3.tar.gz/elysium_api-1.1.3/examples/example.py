from elysium_api import ElysiumApi

# Inicialização da API
api = ElysiumApi({
    "email": "seu-email@exemplo.com",
    "hash": "seu-hash-de-autenticacao"
})

# Exemplo de criação de cliente
try:
    cliente = api.create_client({
        "nome": "Fernando",
        "numero": "000000000",
        "plano_id": "264",
        "email_cliente": "teste@gmail.com",
        "vencimento": "2025-10-31",
        "observacao": "Observação"
    })
    print("Cliente criado:", cliente)
except Exception as error:
    print("Erro:", error)

# Exemplo de listagem de planos
try:
    planos = api.list_plans(search="premium", page=1, limit=10)
    print("Planos encontrados:", planos)
except Exception as error:
    print("Erro:", error)