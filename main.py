from fastapi import FastAPI
from src.web.auth.auth_middlewares import AuthMiddleware
from src.infrastructure.config.application_container import AplicationContainer
from starlette.middleware.cors import CORSMiddleware
import src.web.auth.auth_router as auth_router
# import src.web.stock.stock_router as stock_router
# import src.web.stock.stock_ws as stock_ws
from src.infrastructure.utils.class_object import singleton


@singleton
class AppCreator:
    def __init__(self):
        # set container
        self.container = AplicationContainer()
        self.settings = self.container.settings()

        # set app default
        self.app = FastAPI()

        # set cors
        if self.settings.CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in self.settings.CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # set auth middleware
        self.app.add_middleware(AuthMiddleware)

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"
        
        # self.app.include_router(stock_router.router)
        # self.app.include_router(stock_ws.router)
        self.app.include_router(auth_router.router)


app_creator = AppCreator()
app = app_creator.app
container = app_creator.container
