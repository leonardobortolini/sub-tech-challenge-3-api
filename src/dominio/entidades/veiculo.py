from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.dominio.enums.status import StatusVeiculo
from src.dominio.excecoes.excecoes import VeiculoJaVendido

# Entidade que representa um veiculo
@dataclass
class Veiculo:

    id: UUID
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal
    status: StatusVeiculo = StatusVeiculo.DISPONIVEL

    # Valida se ja foi vendido
    def vender(self):

        if self.status == StatusVeiculo.VENDIDO:
            raise VeiculoJaVendido()

        self.status = StatusVeiculo.VENDIDO