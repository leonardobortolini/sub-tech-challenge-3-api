from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import configuracoes

# Cria conexao com o banco
engine = create_engine(
    configuracoes.DATABASE_URL
)


# Criacao das sessoes do banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Criacao dos modelos
Base = declarative_base()



def obter_sessao():

    sessao = SessionLocal()

    try:
        yield sessao

    finally:
        sessao.close()