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

    MINIO_HOST: str
    MINIO_URL: str
    MINIO_PORT: int
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str

    HASH_SALT: str
    HASH_ALGO: str
    IDX_LEN: int


settings = Settings()
