import httpx

from jose import jwt

from src.infraestrutura.autenticacao.configuracao import (
    JWKS_URL,
    ISSUER,
    KEYCLOAK_CLIENT_ID
)


def obter_chaves_publicas():

    resposta = httpx.get(
        JWKS_URL
    )

    resposta.raise_for_status()

    return resposta.json()