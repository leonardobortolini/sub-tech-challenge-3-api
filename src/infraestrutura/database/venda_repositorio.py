from src.dominio.entidades.venda import Venda
from src.dominio.enums.status import StatusPagamento

from src.infraestrutura.database.modelos import VendaModelo


class VendaRepositorioPostgres:


    def __init__(
        self,
        sessao
    ):
        self.sessao = sessao


    def salvar(
        self,
        venda: Venda
    ):

        # Busca venda existente
        modelo = (
            self.sessao
            .query(VendaModelo)
            .filter_by(id=venda.id)
            .first()
        )

        # Cria caso nao exista
        if not modelo:

            modelo = VendaModelo(
                id=venda.id
            )

        # Atualiza dados
        modelo.veiculo_id = venda.veiculo_id
        modelo.keycloak_user_id = venda.keycloak_user_id
        modelo.cpf_comprador = venda.cpf_comprador
        modelo.codigo_pagamento = venda.codigo_pagamento
        modelo.data_venda = venda.data_venda
        modelo.status_pagamento = venda.status_pagamento.value


        self.sessao.add(
            modelo
        )

        self.sessao.commit()

    # Busca pelo codigo de pagamento
    def buscar_por_codigo_pagamento(
        self,
        codigo
    ):

        modelo = (
            self.sessao
            .query(VendaModelo)
            .filter_by(
                codigo_pagamento=codigo
            )
            .first()
        )


        if not modelo:
            return None


        return Venda(
            id=modelo.id,
            veiculo_id=modelo.veiculo_id,
            keycloak_user_id=modelo.keycloak_user_id,
            cpf_comprador=modelo.cpf_comprador,
            codigo_pagamento=modelo.codigo_pagamento,
            data_venda=modelo.data_venda,
            status_pagamento=StatusPagamento(
                modelo.status_pagamento
            )
        )

    def listar_por_status_pagamento(
        self,
        status
    ):
        # Busca vendas pelo status
        vendas = (
            self.sessao
            .query(VendaModelo)
            .filter_by(
                status_pagamento=status
            )
            .all()
        )


        return [
            Venda(
                id=venda.id,
                veiculo_id=venda.veiculo_id,
                keycloak_user_id=venda.keycloak_user_id,
                cpf_comprador=venda.cpf_comprador,
                codigo_pagamento=venda.codigo_pagamento,
                data_venda=venda.data_venda,
                status_pagamento=StatusPagamento(
                    venda.status_pagamento
                )
            )

            for venda in vendas
        ]