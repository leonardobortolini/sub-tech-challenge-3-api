from uuid import uuid4

from src.dominio.entidades.venda import Venda
from src.dominio.validacao.cpf import CPF
from src.dominio.excecoes.excecoes import VeiculoNaoEncontrado

# Realizar venda
class VenderVeiculo:


    def __init__(
        self,
        veiculo_repositorio,
        venda_repositorio
    ):

        self.veiculo_repositorio = veiculo_repositorio
        self.venda_repositorio = venda_repositorio


    def executar(
        self,
        veiculo_id,
        cpf_comprador,
        data_venda
    ):
        # Busca pelo id
        veiculo = (
            self.veiculo_repositorio
            .buscar_por_id(
                veiculo_id
            )
        )


        if not veiculo:

            raise VeiculoNaoEncontrado()


        # Valida o CPF
        cpf_validado = CPF(
            cpf_comprador
        )


        # Atualiza o status do veiculo para vendido
        veiculo.vender()

        # Cria venda
        venda = Venda(
            id=uuid4(),
            veiculo_id=veiculo.id,
            cpf_comprador=str(
                cpf_validado
            ),
            codigo_pagamento=str(
                uuid4()
            ),
            data_venda=data_venda
        )


        self.veiculo_repositorio.salvar(
            veiculo
        )


        self.venda_repositorio.salvar(
            venda
        )


        return venda