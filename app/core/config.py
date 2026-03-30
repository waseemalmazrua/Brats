from pydantic_settings import BaseSettings, SettingsConfigDict

import os
class Setting(BaseSettings):
    DATABASE_URL: str
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
        env_file=os.getenv("ENV_FILE", ".env"), env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Setting()
