from decimal import Decimal
from uuid import uuid4

import pytest

from src.dominio.entidades.veiculo import Veiculo
from src.dominio.enums.status import StatusVeiculo
from src.dominio.excecoes.excecoes import VeiculoJaVendido


# Cria um veículo padrão
def criar_veiculo():
    return Veiculo(
        id=uuid4(),
        marca="Toyota",
        modelo="Corolla",
        ano=2025,
        cor="Preto",
        preco=Decimal("120000.00")
    )

# Testa se um veículo disponível pode ser vendido
def test_veiculo_disponivel_pode_ser_vendido():

    veiculo = criar_veiculo()

    veiculo.vender()

    assert veiculo.status == StatusVeiculo.VENDIDO


# Testa se um veículo que já foi vendido não pode ser vendido novamente
def test_veiculo_vendido_nao_pode_ser_vendido_novamente():

    veiculo = criar_veiculo()

    veiculo.vender()

    with pytest.raises(VeiculoJaVendido):
        veiculo.vender()