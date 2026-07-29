from fastapi import FastAPI

from src.apresentacao.controllers import (
    veiculos,
    pagamentos
)

from src.infraestrutura.database.conexao import (
    Base,
    engine
)

from src.infraestrutura.database import modelos


# Cria as tabelas no banco
Base.metadata.create_all(
    bind=engine
)

# Inicializa aplicacao
app = FastAPI(
    title="Revenda Veiculos API",
    description="API para gerenciamento de venda de veículos",
    version="1.0.0"
)

# Registra rotas de veiculos
app.include_router(
    veiculos.router
)

# Registra rotas de pagamentos
app.include_router(
    pagamentos.router
)

# Status da aplicacao
@app.get("/health")
def health_check():

    return {
        "status": "OK"
    }