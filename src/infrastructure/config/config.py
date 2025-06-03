import os
from typing import Iterable

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

ENV: str = ""


class Configs(BaseSettings):
    # base
    ENV: str = os.getenv("ENV", "dev")
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'cashcat-backend')
    PORT: int = int(os.getenv('PORT', '8000'))
    VERSION: str = os.getenv('VERSION', '0.0.1')
    ENV_DATABASE_MAPPER: dict = {
        "prod": "cashcat-prod",
        "stage": "cashcat-stage",
        "dev": "cashcat-dev",
        "test": "cashcat-test",
    }
    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
        "sqlite": "sqlite",
    }

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # CORS
    CORS_ORIGINS: Iterable[str] = os.getenv('CORS_ORIGINS', '').split(',')

    # auth
    SUPABASE_URL: str = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY: str = os.getenv('SUPABASE_KEY', '')

    # external services
    STOCK_API_BASE_URL: str = os.getenv('STOCK_API_BASE_URL', '')
    STOCK_API_TOKEN: str = os.getenv('STOCK_API_TOKEN', '')
    HISTORIC_STOCK_API_BASE_URL: str = os.getenv('HISTORIC_STOCK_API_BASE_URL', '')
    HISTORIC_STOCK_API_TOKEN: str = os.getenv('HISTORIC_STOCK_API_TOKEN', '')

    # database
    DB: str = os.getenv("DB", "postgresql")
    DB_USER: str = os.getenv("DB_USER", "admin")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "admin")
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "postgresql")

    DATABASE_URI_FORMAT: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}"

    DATABASE_URI: str = DATABASE_URI_FORMAT.format(
        db_engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=ENV_DATABASE_MAPPER[ENV],
    )

    class Config:
        case_sensitive = True


class TestConfigs(Configs):
    ENV: str = "test"


configs = Configs()

if ENV == "prod":
    pass
elif ENV == "stage":
    pass
elif ENV == "test":
    setting = TestConfigs()