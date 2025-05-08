from typing import Literal

# во 2 версии Pydantic модуль BaseSettings
# был вынесен в отдельную библиотеку pydantic-settings
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict


# TODO: more classes for different types of settings (db, general etc)
class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    NAME_CONVENTION: dict = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    EXCEPTION_TEXT_BY_MODEL: dict = {
        "Class": "Такое занятие",
        "User": "Пользователь с такой почтой",
        "Lesson": "Такой урок",
    }

    SLUGIFY_ATTR_BY_MODEL: dict = {
        "Class": "name",
        "User": "name",
        "Lesson": "name",
        "Word": "hiragana",
    }

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # TEST_DB_HOST: str
    # TEST_DB_PORT: int
    # TEST_DB_USER: str
    # TEST_DB_PASS: str
    # TEST_DB_NAME: str

    # @property
    # def TEST_DATABASE_URL(self):
    #     return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    # SMTP_HOST: str
    # SMTP_PORT: int
    # SMTP_USER: str
    # SMTP_PASS: str

    # REDIS_HOST: str
    # REDIS_PORT: int

    # SENTRY_DSN: str

    SECRET_KEY: str
    ALGORITHM: str

    # Со 2 версии Pydantic, class Config был заменен на атрибут model_config
    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
