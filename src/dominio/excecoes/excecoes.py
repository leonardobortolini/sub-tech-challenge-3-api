# Excecao para veiculo nao encontrado
class VeiculoNaoEncontrado(Exception):

    def __init__(
        self
    ):

        super().__init__(
            "Veiculo nao encontrado"
        )


# Excecao para veiculo ja vendido
class VeiculoJaVendido(Exception):

    def __init__(
        self
    ):

        super().__init__(
            "Veiculo ja vendido"
        )


# Excecao para pagamento nao encontrado
class PagamentoNaoEncontrado(Exception):

    def __init__(
        self
    ):

        super().__init__(
            "Pagamento nao encontrado"
        )