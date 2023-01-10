import pathlib
from typing import Literal

from pydantic import BaseSettings, Field

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()


class BaseSettingsDotEnv(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DB(BaseSettingsDotEnv):
    host: str = Field(..., env="DATABASE_HOST")
    port: int = Field(..., env="DATABASE_PORT")
    db: str = Field(..., env="DATABASE_NAME")
    user: str = Field(..., env="DATABASE_USER")
    password: str = Field(..., env="DATABASE_PASSWORD")


class RabbitMQ(BaseSettingsDotEnv):
    host: str = Field(..., env="RABBIT_MQ_HOST")
    port: int = Field(..., env="RABBIT_MQ_PORT")
    user: str = Field(..., env="RABBIT_MQ_USER")
    password: str = Field(..., env="RABBIT_MQ_PASSWORD")
    queue: str = Field(..., env="RABBIT_MQ_QUEUE")


class Settings(BaseSettingsDotEnv):
    log_level: Literal["DEBUG", "INFO"] = Field("INFO", env="LOG_LEVEL")
    environment: Literal["localdev", "stg", "prod"] = Field(..., env="ENVIRONMENT")
    BACKEND_CORS_ORIGINS: list[str] = Field(..., env="BACKEND_CORS_ORIGINS")
    db: DB = Field(default_factory=DB)
    rabbit_mq: RabbitMQ = Field(default_factory=RabbitMQ)


settings = Settings()
