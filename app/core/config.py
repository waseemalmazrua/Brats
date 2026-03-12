from pydantic import BaseSettings , SettingConfigDict


class Setting(BaseSettings):


    DATABASE_URL: str

    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str

    model_config = SettingConfigDict(env_file=".env", env_file_encoding="utf-8",casesenstive=False , extra="ignore")

settings = Setting()
