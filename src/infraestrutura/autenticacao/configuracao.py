from src.config import configuracoes

# COnfiguracoes utilizadas na autenticacao com o keycloak

KEYCLOAK_INTERNAL_URL = (
    configuracoes.KEYCLOAK_INTERNAL_URL
)

KEYCLOAK_REALM = (
    configuracoes.KEYCLOAK_REALM
)

KEYCLOAK_CLIENT_ID = (
    configuracoes.KEYCLOAK_CLIENT_ID
)


JWKS_URL = (
    f"{KEYCLOAK_INTERNAL_URL}"
    f"/realms/{KEYCLOAK_REALM}"
    f"/protocol/openid-connect/certs"
)

ISSUERS_VALIDOS = [
    configuracoes.KEYCLOAK_ISSUER,
    configuracoes.KEYCLOAK_EXTERNAL_ISSUER,
]