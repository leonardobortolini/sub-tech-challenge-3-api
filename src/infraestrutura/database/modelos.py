from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.infraestrutura.database.conexao import Base

# Modelo da tabela veiculos
class VeiculoModelo(Base):

    __tablename__ = "veiculos"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    marca = Column(String)
    modelo = Column(String)
    ano = Column(Integer)
    cor = Column(String)
    preco = Column(Numeric)

    status = Column(String)


# Modelo da tabela vendas
class VendaModelo(Base):

    __tablename__ = "vendas"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    veiculo_id = Column(
        UUID(as_uuid=True),
        ForeignKey("veiculos.id")
    )


    cpf_comprador = Column(String)

    codigo_pagamento = Column(String)

    data_venda = Column(DateTime)

    status_pagamento = Column(String)