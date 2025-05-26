from typing import Annotated, List
from fastapi import APIRouter, Depends, Request
from src.stocks.service import StockService
from core.infrastructure.di.containers import AplicationContainer
from dependency_injector.wiring import Provide, inject

from src.stocks.models import STOCKS_PREFIX, StockQuote

router = APIRouter(prefix=f'/{STOCKS_PREFIX}', tags=[STOCKS_PREFIX])

@router.get("/")
async def get_stocks(
    request: Request
):
    user = request.state.current_user
    return {"message": "Lista de stocks", "user": user}


@router.get("/{stock_symbol}/current", response_model=StockQuote)
@inject
async def get_stock(
    stock_symbol: str,
    stock_service: Annotated[
        StockService,
        Depends(Provide[AplicationContainer.stocks_package.stock_service])
    ]
):
    return await stock_service.get_current_stock_price(stock_symbol)


@router.get("/{stock_symbol}/historic", response_model=List[StockQuote])
@inject
async def get_historic_stock(
    stock_symbol: str,
    from_timestamp: int,
    to_timestamp: int,
    group_by: str,
    stock_service: Annotated[
        StockService, Depends(Provide[AplicationContainer.stocks_package.stock_service])
    ]
):
    return await stock_service.get_historic_stock_price(
        symbol=stock_symbol,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        group_by=group_by
    )
