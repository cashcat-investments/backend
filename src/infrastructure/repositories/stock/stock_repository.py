from datetime import datetime
from typing import List
from src.stocks.models import StockQuote

from src.infrastructure.shared.http.http_client import HTTPClient

class StockRepository:

    def __init__(self, stock_api: HTTPClient, historic_stock_api: HTTPClient):
        self._stock_api = stock_api
        self._historic_stock_api = historic_stock_api


    async def get_current_stock_price(self, symbol: str) -> StockQuote:
        response = await self._stock_api.get(path="/quote", params={
            "symbol": symbol,
        })
        return StockQuote(
            price=response["c"],
            timestamp=datetime.fromtimestamp(response["t"])
        )


    async def get_historic_stock_price(
        self,
        symbol: str,
        from_timestamp: int,
        to_timestamp: int,
        group_by: str
    ) -> List[StockQuote]:
        response = await self._historic_stock_api.get(
            path=f'/aggs/ticker/{symbol}/range/1/{group_by}/{from_timestamp}/{to_timestamp}',
            params={
                "adjusted": "true",
                "sort": "asc",
            }
        )

        return [
            StockQuote(
                price=item["c"],
                timestamp=datetime.fromtimestamp(item["t"] / 1000)
            ) for item in response["results"]
        ]
