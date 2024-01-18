from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")
    user: str = "postgres"
    password: str = "postgres"
    name: str = "postgres"
    host: str = "localhost"
    port: int = 5432


class Settings(BaseSettings):
    shared_schema: str = 'public'
    tenant_schema: str = 'tenant'


def get_database_settings() -> DataBaseSettings:
    return DataBaseSettings()
