from dependency_injector import containers, providers

from src.modules.auth.infrastructure.supabase.supabase_auth_repository import SupabaseAuthRepository
from src.modules.auth.application.auth_service import AuthService
from src.core.infrastructure.supabase.supabase import Supabase

class AuthContainer(containers.DeclarativeContainer):
    supabase = providers.Dependency(Supabase)

    auth_repository = providers.Singleton(
        SupabaseAuthRepository,
        supabase=supabase
    )

    auth_service = providers.Singleton(
        AuthService,
        auth_repository=auth_repository
    )
