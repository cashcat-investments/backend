from dependency_injector import containers, providers

from src.stocks.service import StockService
from src.utils.http_client import HTTPClient
from src.settings import Settings
from src.stocks.repositories import StockRepository

class StocksContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(Settings)

    stock_api = providers.Singleton(
        HTTPClient,
        base_url=settings.instance_of().STOCK_API_BASE_URL,
        headers={
            "X-Finnhub-Token": settings.instance_of().STOCK_API_TOKEN
        }
    )

    historic_stock_api = providers.Singleton(
        HTTPClient,
        base_url=settings.instance_of().HISTORIC_STOCK_API_BASE_URL,
        params={
            "apiKey": settings.instance_of().HISTORIC_STOCK_API_TOKEN
        }
    )

    stock_repository = providers.Singleton(
        StockRepository,
        stock_api=stock_api,
        historic_stock_api=historic_stock_api
    )

    stock_service = providers.Singleton(
        StockService,
        stock_repository=stock_repository
    )
