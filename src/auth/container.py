from dependency_injector import containers, providers

from src.auth.repositories import AuthRepository
from src.auth.service import AuthService
from src.utils.supabase import Supabase

class AuthContainer(containers.DeclarativeContainer):
    supabase = providers.Dependency(Supabase)

    auth_repository = providers.Singleton(
        AuthRepository,
        supabase=supabase
    )

    auth_service = providers.Singleton(
        AuthService,
        auth_repository=auth_repository
    )
