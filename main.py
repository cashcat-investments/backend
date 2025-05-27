from fastapi import FastAPI
from modules.auth.auth_middlewares import AuthMiddleware
from src.core.infrastructure.di.application_container import AplicationContainer
from starlette.middleware.cors import CORSMiddleware
# import src.stocks.router as stocks_router
# import src.stocks.ws as stocks_ws_router
import modules.auth.auth_router as auth_router
from src.core.infrastructure.utils.class_object import singleton



@singleton
class AppCreator:
    def __init__(self):
        # set container
        self.container = AplicationContainer()
        self.settings = self.container.settings()

        # set app default
        self.app = FastAPI()

        # set db
        # self.db = self.container.db()
        # self.db.create_database()

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
        
        # self.app.include_router(stocks_router.router)
        # self.app.include_router(stocks_ws_router.router)
        self.app.include_router(auth_router.router)


app_creator = AppCreator()
app = app_creator.app
# db = app_creator.db
container = app_creator.container
