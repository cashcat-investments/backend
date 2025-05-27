from dependency_injector import containers, providers
from supabase import create_client

from src.core.infrastructure.config.settings import Settings
from src.core.infrastructure.db.database import Database
from src.modules.auth.infrastructure.repositories.auth_repository import AuthRepository
from application.services.auth_service import AuthService
from src.infrastructure.shared.http.http_client import HTTPClient

class AplicationContainer(containers.DeclarativeContainer):
    # wiring config
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.modules.auth.infrastructure.web.auth_router"
        ]
    )

    # env variables and project settings
    settings = providers.Singleton(Settings)

    # clients and sessions
    supabase = providers.Singleton(
        create_client,
        settings().SUPABASE_URL,
        settings().SUPABASE_KEY
    )
    db = providers.Singleton(Database, db_url=settings().DATABASE_URL)
    stock_api = providers.Singleton(
        HTTPClient,
        base_url=settings().STOCK_API_BASE_URL,
        headers={
            "X-Finnhub-Token": settings().STOCK_API_TOKEN
        }
    )
    historic_stock_api = providers.Singleton(
        HTTPClient,
        base_url=settings().HISTORIC_STOCK_API_BASE_URL,
        params={
            "apiKey": settings().HISTORIC_STOCK_API_TOKEN
        }
    )

    # repositories
    auth_repository = providers.Factory(
        AuthRepository,
        supabase=supabase
    )

    # stock_repository = providers.Singleton(
    #     StockRepository,
    #     stock_api=stock_api,
    #     historic_stock_api=historic_stock_api
    # )

    # stock_service = providers.Singleton(
    #     StockService,
    #     stock_repository=stock_repository
    # )

    # services
    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository
    )
