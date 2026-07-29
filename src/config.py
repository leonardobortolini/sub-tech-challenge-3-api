from pydantic_settings import BaseSettings


class Configuracoes(BaseSettings):

    DATABASE_URL: str


    class Config:
        env_file = ".env"


configuracoes = Configuracoes()