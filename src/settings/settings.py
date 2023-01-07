from typing import Optional
from pydantic import BaseSettings


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
    sub: str


class ProjectSettings(BaseSettings):
    db: ProjectDatabase
    jwt: ProjectAuthentication

    class Config:
        env_file: str = ".env"
        env_nested_delimiter = "__"
        case_sensitive: False


__settings: Optional[ProjectSettings] = None


async def load_settings() -> Optional[ProjectSettings]:
    global __settings
    __settings = ProjectSettings()


async def get_settings() -> Optional[ProjectSettings]:
    global __settings
    if not __settings:
        raise Exception("Project settings are not loaded")
    return __settings
