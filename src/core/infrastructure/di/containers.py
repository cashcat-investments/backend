from dependency_injector import containers, providers

from src.core.infrastructure.config.settings import Settings
from src.modules.auth.infrastructure.di.auth_container import AuthContainer
# from src.stocks.container import StocksContainer
from src.core.infrastructure.supabase.supabase import Supabase

class AplicationContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    supabase = providers.Singleton(
        Supabase,
        settings=settings
    )
    # stocks_package = providers.Container(
    #     StocksContainer,
    #     settings=settings
    # )
    auth_package = providers.Container(
        AuthContainer,
        supabase=supabase,
    )
