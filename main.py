from fastapi import FastAPI
from src.auth.middleware import AuthMiddleware
from src.containers import AplicationContainer
from starlette.middleware.cors import CORSMiddleware
import src.stocks.router as stocks_router
import src.stocks.ws as stocks_ws_router
import src.auth.router as auth_router

def create_app() -> FastAPI:
    container = AplicationContainer()
    container.wire(modules=[
        stocks_router,
        stocks_ws_router,
        auth_router
    ])

    fastapi_app = FastAPI()

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi_app.add_middleware(AuthMiddleware)

    fastapi_app.include_router(stocks_router.router)
    fastapi_app.include_router(stocks_ws_router.router)
    fastapi_app.include_router(auth_router.router)
    return fastapi_app

app = create_app()
