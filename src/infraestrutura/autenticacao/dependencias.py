from fastapi import Depends

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from src.infraestrutura.autenticacao.autenticacao import (
    validar_token
)

# Autenticacao Bearer
bearer_scheme = HTTPBearer()


def obter_usuario_autenticado(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
):

    # Token enviado na requisicao
    token = credentials.credentials

    # Valida o token e retorna os dados do usuário
    return validar_token(
        token
    )