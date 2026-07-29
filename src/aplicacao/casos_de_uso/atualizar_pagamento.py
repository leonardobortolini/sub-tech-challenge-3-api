from src.dominio.enums.status import StatusPagamento
from src.dominio.excecoes.excecoes import PagamentoNaoEncontrado

# Atualiza status de um pagamento
class AtualizarPagamento:


    def __init__(
        self,
        venda_repositorio
    ):

        self.venda_repositorio = venda_repositorio


    def executar(
        self,
        codigo_pagamento,
        status
    ):

        # Busca venda pelo código do pagamento
        venda = (
            self.venda_repositorio
            .buscar_por_codigo_pagamento(
                codigo_pagamento
            )
        )


        if not venda:

            raise PagamentoNaoEncontrado()


        venda.atualizar_pagamento(
            StatusPagamento(status)
        )


        self.venda_repositorio.salvar(
            venda
        )


        return venda