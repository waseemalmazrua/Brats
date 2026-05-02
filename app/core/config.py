
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Setting(BaseSettings):
    DATABASE_URL: str
    DATABASE_URL_PROD: Optional[str] = None
    IS_DEV: bool = True  
    @property
    def db_url(self) -> str:
        return self.DATABASE_URL if self.IS_DEV else self.DATABASE_URL_PROD

    ALGORITHM: str

    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str

    MLFLOW_MODEL_URI: str
    BENTO_MODEL_NAME : str
    MLFLOW_TRACKING_URI: str

    BENTOML_MODEL_TAG: str
    BENTO_URL: str

    GOOGLE_APPLICATION_CREDENTIALS: str

    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Setting()
