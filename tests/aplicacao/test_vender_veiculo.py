from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.aplicacao.casos_de_uso.vender_veiculo import VenderVeiculo
from src.dominio.entidades.veiculo import Veiculo
from src.dominio.enums.status import StatusVeiculo, StatusPagamento
from src.dominio.excecoes.excecoes import (
    VeiculoNaoEncontrado,
    VeiculoJaVendido
)


class FakeVeiculoRepositorio:

    def __init__(self, veiculo=None):

        self.veiculo = veiculo

        self.veiculo_salvo = None


    # Simula a busca de um veículo pelo id
    def buscar_por_id(self, id):

        if self.veiculo and self.veiculo.id == id:
            return self.veiculo

        return None


    # Simula a persistência
    def salvar(self, veiculo):

        self.veiculo_salvo = veiculo


class FakeVendaRepositorio:

    def __init__(self):

        # Armazena a venda enviada para persistência durante o teste
        self.venda_salva = None


    # Simula a persistência de uma venda
    def salvar(self, venda):

        self.venda_salva = venda


# Cria um veículo padrão
def criar_veiculo():

    return Veiculo(
        id=uuid4(),
        marca="Toyota",
        modelo="Corolla",
        ano=2025,
        cor="Preto",
        preco=Decimal("120000.00"),
        status=StatusVeiculo.DISPONIVEL
    )


# Testa se uma venda é realizada corretamente quando todos os dados são válidos
def test_deve_realizar_venda():

    veiculo = criar_veiculo()

    veiculo_repo = FakeVeiculoRepositorio(
        veiculo
    )

    venda_repo = FakeVendaRepositorio()

    caso_de_uso = VenderVeiculo(
        veiculo_repo,
        venda_repo
    )

    data_venda = datetime(
        2026,
        8,
        13,
        15,
        0
    )

    # Executa o caso de uso de venda do veículo
    venda = caso_de_uso.executar(
        veiculo_id=veiculo.id,
        keycloak_user_id="usuario-keycloak-123",
        cpf_comprador="24489006047",
        data_venda=data_venda
    )

    # Verifica se a venda está associada ao veículo correto
    assert venda.veiculo_id == veiculo.id

    # Verifica se o usuário responsável pela venda foi armazenado corretamente
    assert venda.keycloak_user_id == "usuario-keycloak-123"

    # Verifica se o CPF do comprador foi armazenado corretamente
    assert venda.cpf_comprador == "24489006047"

    # Verifica se a data informada foi utilizada na venda
    assert venda.data_venda == data_venda

    # Uma nova venda deve iniciar com o pagamento pendente
    assert venda.status_pagamento == StatusPagamento.PENDENTE

    # Após a venda, o status do veículo deve ser alterado para vendido
    assert veiculo.status == StatusVeiculo.VENDIDO

    # Verifica se o veículo alterado foi enviado para persistência
    assert veiculo_repo.veiculo_salvo == veiculo

    # Verifica se a venda criada foi enviada para persistência
    assert venda_repo.venda_salva == venda


# Testa se o sistema impede a venda quando o veículo não existe
def test_nao_deve_vender_veiculo_inexistente():

    veiculo_repo = FakeVeiculoRepositorio()

    venda_repo = FakeVendaRepositorio()

    caso_de_uso = VenderVeiculo(
        veiculo_repo,
        venda_repo
    )

    # Tentar vender um veículo inexistente deve gerar uma exceção
    with pytest.raises(VeiculoNaoEncontrado):

        caso_de_uso.executar(
            veiculo_id=uuid4(),
            keycloak_user_id="usuario-keycloak-123",
            cpf_comprador="24489006047",
            data_venda=datetime.now()
        )


# Testa se o sistema impede a venda de um veículo que já foi vendido
def test_nao_deve_vender_veiculo_ja_vendido():

    veiculo = criar_veiculo()

    veiculo.vender()

    veiculo_repo = FakeVeiculoRepositorio(
        veiculo
    )

    venda_repo = FakeVendaRepositorio()

    caso_de_uso = VenderVeiculo(
        veiculo_repo,
        venda_repo
    )

    # Tentar vender novamente deve gerar uma exceção
    with pytest.raises(VeiculoJaVendido):

        caso_de_uso.executar(
            veiculo_id=veiculo.id,
            keycloak_user_id="usuario-keycloak-123",
            cpf_comprador="24489006047",
            data_venda=datetime.now()
        )


# Testa se o sistema rejeita uma venda quando o CPF informado é inválido
def test_nao_deve_realizar_venda_com_cpf_invalido():

    veiculo = criar_veiculo()

    veiculo_repo = FakeVeiculoRepositorio(
        veiculo
    )

    venda_repo = FakeVendaRepositorio()

    caso_de_uso = VenderVeiculo(
        veiculo_repo,
        venda_repo
    )

    # Venda com CPF inválido deve gerar um erro
    with pytest.raises(ValueError):

        caso_de_uso.executar(
            veiculo_id=veiculo.id,
            keycloak_user_id="usuario-keycloak-123",
            cpf_comprador="24489776047",
            data_venda=datetime.now()
        )

    # O veículo não deve ser alterado quando a venda falha na validação
    assert veiculo.status == StatusVeiculo.DISPONIVEL

    # Nenhuma venda deve ser persistida quando o CPF é inválido
    assert venda_repo.venda_salva is None