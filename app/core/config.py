from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DATABASE_URL: str
    ALGORITHM: str

    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str

    MLFLOW_MODEL_URI: str
    BENTO_MODEL_NAME : str
    MLFLOW_TRACKING_URI: str

    GOOGLE_APPLICATION_CREDENTIALS: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", casesenstive=False, extra="ignore"
    )


settings = Setting()
