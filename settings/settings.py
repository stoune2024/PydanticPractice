from email.policy import default

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DB_HOST: str = Field(default='postgres')
    DB_PORT: str = Field(default='5432')
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=f"{os.path.dirname(os.path.abspath(__file__))}/../.env"
    )

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()