import asyncio
from datetime import datetime
from typing import List
from fastapi import WebSocket
from src.stocks.models import StockQuote
from src.stocks.repositories import StockRepository


class StockService:

    def __init__(self, stock_repository: StockRepository):
        self._stock_repository = stock_repository
        self._polling_running = False


    async def get_current_stock_price(self, symbol: str) -> StockQuote:
        return await self._stock_repository.get_current_stock_price(symbol)


    async def start_current_stock_price_polling(self, websocket: WebSocket, symbol: str):
        if self._polling_running:
            return
        
        self._polling_running = True

        while self._polling_running:
            updated_data = await self.get_current_stock_price(symbol)
            updated_data.timestamp = datetime.now()
            await websocket.send_json({
                "symbol": symbol,
                "data": updated_data.to_dict(),
            })
            await asyncio.sleep(30)


    async def stop_current_stock_price_polling(self):
        self._polling_running = False


    async def get_historic_stock_price(
        self,
        symbol: str,
        from_timestamp: int,
        to_timestamp: int,
        group_by: str
    ) -> List[StockQuote]:
        return await self._stock_repository.get_historic_stock_price(
            symbol,
            from_timestamp,
            to_timestamp,
            group_by
        )
