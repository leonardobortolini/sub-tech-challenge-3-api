from decimal import Decimal
from uuid import UUID
from datetime import datetime


from pydantic import BaseModel

# Dados de cadastro de veiculo
class CriarVeiculoRequest(BaseModel):

    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal


# Dados do veiculo retornados
class VeiculoResponse(BaseModel):

    id: UUID

    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal
    status: str


# Dados de veiculo vendido
class VeiculoVendidoResponse(BaseModel):

    id: UUID

    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal

    cpf_comprador: str
    data_venda: datetime
    status_pagamento: str