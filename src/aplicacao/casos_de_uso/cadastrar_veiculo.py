from uuid import uuid4

from src.dominio.entidades.veiculo import Veiculo

# Cadastro de veículo
class CadastrarVeiculo:


    def __init__(
        self,
        veiculo_repositorio
    ):
        self.veiculo_repositorio = veiculo_repositorio


    def executar(
        self,
        marca,
        modelo,
        ano,
        cor,
        preco
    ):
        # Cria veículo
        veiculo = Veiculo(
            id=uuid4(),
            marca=marca,
            modelo=modelo,
            ano=ano,
            cor=cor,
            preco=preco
        )

        # Salva
        self.veiculo_repositorio.salvar(
            veiculo
        )


        return veiculo
