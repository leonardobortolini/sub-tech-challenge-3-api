# Listar pagamentos
class ListarPagamentos:


    def __init__(
        self,
        venda_repositorio
    ):

        self.venda_repositorio = venda_repositorio



    def executar(
        self,
        status
    ):

        return (
            self.venda_repositorio
            .listar_por_status_pagamento(
                status
            )
        )