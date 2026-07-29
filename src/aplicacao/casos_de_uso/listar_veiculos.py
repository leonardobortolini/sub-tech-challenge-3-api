# Listar veiculos
class ListarVeiculos:


    def __init__(
        self,
        veiculo_repositorio
    ):

        self.veiculo_repositorio = veiculo_repositorio



    def disponiveis(
        self
    ):

        return (
            self.veiculo_repositorio
            .listar_disponiveis()
        )


    def vendidos(
        self
    ):

        return (
            self.veiculo_repositorio
            .listar_vendidos()
        )
