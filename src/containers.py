from dependency_injector import containers, providers

from src.settings import Settings
from src.auth.container import AuthContainer
from src.stocks.container import StocksContainer
from src.utils.supabase import Supabase

class AplicationContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    supabase = providers.Singleton(
        Supabase,
        settings=settings
    )
    stocks_package = providers.Container(
        StocksContainer,
        settings=settings
    )
    auth_package = providers.Container(
        AuthContainer,
        supabase=supabase,
    )
