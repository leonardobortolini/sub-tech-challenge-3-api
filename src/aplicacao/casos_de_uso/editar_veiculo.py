from src.dominio.excecoes.excecoes import VeiculoNaoEncontrado


# Editar veiculo
class EditarVeiculo:


    def __init__(
        self,
        veiculo_repositorio
    ):
        self.veiculo_repositorio = veiculo_repositorio



    def executar(
        self,
        id,
        marca,
        modelo,
        ano,
        cor,
        preco
    ):

        # BUsca pelo id
        veiculo = (
            self.veiculo_repositorio
            .buscar_por_id(id)
        )

        # Confere se o veículo existe
        if not veiculo:
            raise VeiculoNaoEncontrado()


        # Atualiza dados do veiculo
        veiculo.marca = marca
        veiculo.modelo = modelo
        veiculo.ano = ano
        veiculo.cor = cor
        veiculo.preco = preco


        # Salva
        self.veiculo_repositorio.salvar(
            veiculo
        )


        return veiculo