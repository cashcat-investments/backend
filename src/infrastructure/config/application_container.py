from dependency_injector import containers, providers
from supabase import create_client

from src.infrastructure.repositories.auth.auth_repository import AuthRepository
from src.application.services.auth_service import AuthService
from src.infrastructure.data_sources.http.http_client import HTTPClient
from src.infrastructure.config.settings import Settings
from src.infrastructure.data_sources.db.database import Database
from src.infrastructure.data_sources.db.repositories.user_db_repository import UserDBRepository

class AplicationContainer(containers.DeclarativeContainer):
    # wiring config
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.web.auth.auth_router",
            # "src.web.stock.stock_router",
            # "src.web.stock.stock_ws"
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

    user_repository = providers.Factory(
        UserDBRepository,
        session_factory=db.provided.session
    )

    # stock_repository = providers.Factory(
    #     StockRepository,
    #     stock_api=stock_api,
    #     historic_stock_api=historic_stock_api
    # )

    # stock_service = providers.Factory(
    #     StockService,
    #     stock_repository=stock_repository
    # )

    # services 
    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository,
        user_repository=user_repository
    )
