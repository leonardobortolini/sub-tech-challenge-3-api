from src.dominio.entidades.veiculo import Veiculo
from src.dominio.enums.status import StatusVeiculo

from src.infraestrutura.database.modelos import (
    VeiculoModelo,
    VendaModelo
)


class VeiculoRepositorioPostgres:


    def __init__(
        self,
        sessao
    ):
        self.sessao = sessao


    def salvar(
        self,
        veiculo: Veiculo
    ):

        # Busca veiculo existente
        modelo = (
            self.sessao
            .query(VeiculoModelo)
            .filter_by(id=veiculo.id)
            .first()
        )

        # Cria registro caso nao exista
        if not modelo:

            modelo = VeiculoModelo(
                id=veiculo.id
            )

        # Atualiza dados
        modelo.marca = veiculo.marca
        modelo.modelo = veiculo.modelo
        modelo.ano = veiculo.ano
        modelo.cor = veiculo.cor
        modelo.preco = veiculo.preco
        modelo.status = veiculo.status.value


        self.sessao.add(
            modelo
        )

        self.sessao.commit()


    def buscar_por_id(
        self,
        id
    ):

        # Busca pelo id
        modelo = (
            self.sessao
            .query(VeiculoModelo)
            .filter_by(id=id)
            .first()
        )


        if not modelo:
            return None


        return self._converter_para_entidade(
            modelo
        )


    def listar_disponiveis(
        self
    ):

        # Busca veiculos disponiveis ordenados por preco
        modelos = (
            self.sessao
            .query(VeiculoModelo)
            .filter_by(status="DISPONIVEL")
            .order_by(
                VeiculoModelo.preco.asc()
            )
            .all()
        )


        return [
            self._converter_para_entidade(modelo)
            for modelo in modelos
        ]


    def listar_vendidos(
        self
    ):

        # Busca veiculos vendidos com dados da venda
        registros = (
            self.sessao
            .query(
                VeiculoModelo,
                VendaModelo
            )
            .join(
                VendaModelo,
                VendaModelo.veiculo_id == VeiculoModelo.id
            )
            .filter(
                VeiculoModelo.status == "VENDIDO"
            )
            .order_by(
                VeiculoModelo.preco.asc()
            )
            .all()
        )


        veiculos = []


        # Monta retorno dos veiculos vendidos
        for veiculo, venda in registros:

            veiculos.append(
                {
                    "id": veiculo.id,
                    "marca": veiculo.marca,
                    "modelo": veiculo.modelo,
                    "ano": veiculo.ano,
                    "cor": veiculo.cor,
                    "preco": veiculo.preco,
                    "cpf_comprador": venda.cpf_comprador,
                    "data_venda": venda.data_venda,
                    "status_pagamento": venda.status_pagamento
                }
            )


        return veiculos


    def _converter_para_entidade(
        self,
        modelo
    ):

        return Veiculo(
            id=modelo.id,
            marca=modelo.marca,
            modelo=modelo.modelo,
            ano=modelo.ano,
            cor=modelo.cor,
            preco=modelo.preco,
            status=StatusVeiculo(
                modelo.status
            )
        )