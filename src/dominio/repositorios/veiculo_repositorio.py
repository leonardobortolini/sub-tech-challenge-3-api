from abc import ABC, abstractmethod

from src.dominio.entidades.veiculo import Veiculo

# Repositorio de veiculos
class VeiculoRepositorio(ABC):


    @abstractmethod
    def salvar(
        self,
        veiculo: Veiculo
    ):
        pass


    @abstractmethod
    def buscar_por_id(
        self,
        id
    ):
        pass


    @abstractmethod
    def listar_disponiveis(
        self
    ):
        pass


    @abstractmethod
    def listar_vendidos(
        self
    ):
        pass