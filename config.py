import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from enum import Enum

load_dotenv()


class EnvironmentType(str, Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'


class Settings(BaseSettings):
    DEBUG: int = 1
    APP_NAME: str = 'GSJ Notes'
    APP_VERSION: str = '0.1'
    ADMIN_USERNAME: str = os.getenv('ADMIN_USERNAME')
    ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD')
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    HOST_ADDRESS: str = '0.0.0.0' if DEBUG == 1 else '127.0.0.1'
    HOST_PORT: int = 8000


settings = Settings()
