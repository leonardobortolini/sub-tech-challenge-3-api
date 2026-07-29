from enum import Enum

# Status de um veiculo
class StatusVeiculo(Enum):
    DISPONIVEL = "DISPONIVEL"
    VENDIDO = "VENDIDO"

# Status de um pagamento
class StatusPagamento(Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    CANCELADO = "CANCELADO"