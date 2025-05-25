import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.auth.dependencies import get_websocket_user_session
from src.auth.models import User
from src.stocks.models import STOCKS_PREFIX
from src.stocks.service import StockService
from src.containers import AplicationContainer
from dependency_injector.wiring import Provide, inject
from src.utils.logger import setup_logger

logger = setup_logger('stocks.ws')

router = APIRouter(prefix=f'/{STOCKS_PREFIX}/ws', tags=[f'{STOCKS_PREFIX}-ws'])

@router.websocket("/{stock_symbol}")
@inject
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    stock_symbol: str,
    stock_service: Annotated[
        StockService, Depends(Provide[AplicationContainer.stocks_package.stock_service])
    ],
    session_data: Annotated[
        User, Depends(get_websocket_user_session)
    ]
):
    await websocket.accept()

    try:

        await websocket.send_json({
            "type": "user_info",
            "data": session_data.model_dump()
        })

        # Iniciar el polling de datos
        asyncio.create_task(
            stock_service.start_current_stock_price_polling(
                websocket,
                stock_symbol
            )
        )

        while True:
            #Recibir mensajes del cliente
            message = await websocket.receive_text()
            logger.info(f"Mensaje recibido del cliente para {stock_symbol}: {message}")

    except WebSocketDisconnect:
        logger.info(f"Conexión cerrada para {stock_symbol}")
        await stock_service.stop_current_stock_price_polling()
    finally:
        await stock_service.stop_current_stock_price_polling()