from pydantic import BaseSettings
from functools import lru_cache


class ProjectDatabase(BaseSettings):
    protocol: str
    user: str
    password: str
    host: str
    port: int
    name: str


class ProjectAuthentication(BaseSettings):
    secret: str
    algorithm: str
    expiration: int


class ProjectSettings(BaseSettings):
    db: ProjectDatabase
    jwt: ProjectAuthentication

    class Config:
        env_file: str = ".env"
        env_nested_delimiter = "__"
        case_sensitive: False


@lru_cache
def get_settings() -> ProjectSettings:
    return ProjectSettings()
