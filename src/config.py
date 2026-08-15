from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):

    DATABASE_URL: str

    KEYCLOAK_INTERNAL_URL: str

    KEYCLOAK_ISSUER: str

    KEYCLOAK_EXTERNAL_ISSUER: str

    KEYCLOAK_REALM: str

    KEYCLOAK_CLIENT_ID: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


configuracoes = Configuracoes()