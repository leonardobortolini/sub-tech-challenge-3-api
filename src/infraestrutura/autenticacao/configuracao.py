from src.config import configuracoes


KEYCLOAK_SERVER_URL = (
    configuracoes.KEYCLOAK_SERVER_URL
)

KEYCLOAK_REALM = (
    configuracoes.KEYCLOAK_REALM
)

KEYCLOAK_CLIENT_ID = (
    configuracoes.KEYCLOAK_CLIENT_ID
)


JWKS_URL = (
    f"{KEYCLOAK_SERVER_URL}"
    f"/realms/{KEYCLOAK_REALM}"
    f"/protocol/openid-connect/certs"
)

ISSUER = (
    f"{KEYCLOAK_SERVER_URL}"
    f"/realms/{KEYCLOAK_REALM}"
)