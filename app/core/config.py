from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    APP: str
    HOST: str
    PORT: int

    ENVIRONMENT: str

    MONGO_DB_NAME: str
    MONGO_DB_URI: str

    HASH_SALT: str
    HASH_ALGO: str
    IDX_LEN: int


settings = Settings()
