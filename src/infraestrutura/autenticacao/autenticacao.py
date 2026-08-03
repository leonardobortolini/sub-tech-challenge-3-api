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


def validar_token(token: str):

    cabecalho = jwt.get_unverified_header(
        token
    )

    #baixa chaves públicas
    chaves = obter_chaves_publicas()

    chave = next(
        (
            key
            for key in chaves["keys"]
            if key["kid"] == cabecalho["kid"]
        ),
        None
    )

    if chave is None:

        raise Exception(
            "Chave pública não encontrada."
        )

   #Valida o JWT
    claims = jwt.decode(
        token,
        chave,
        algorithms=["RS256"],
        issuer=ISSUER,
        options={
            "verify_aud": False
        }
    )

    return claims