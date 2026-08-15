from fastapi import FastAPI, Depends

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.infraestrutura.autenticacao.autenticacao import (
    obter_chaves_publicas, validar_token
)

from src.apresentacao.controllers import (
    veiculos,
    pagamentos
)

from src.infraestrutura.database.conexao import (
    Base,
    engine
)

from src.infraestrutura.database import modelos


security = HTTPBearer()


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

@app.get("/teste-keycloak")
def teste():

    return obter_chaves_publicas()

# Status da aplicacao
@app.get("/health")
def health_check():

    return {
        "status": "OK"
    }