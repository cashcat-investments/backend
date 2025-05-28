from supabase import Client
from src.infrastructure.utils.logger import setup_logger
from src.domain.repositories.i_auth_repository import IAuthRepository
from src.domain.entities.auth_entities import CredentialsEntity, AuthResultEntity, TokensEntity, OAuthInputEntity, OAuthResponseEntity
from src.domain.entities.user_entities import UserEntity

logger = setup_logger("AuthRepository")

class AuthRepository(IAuthRepository):
    def __init__(self, supabase: Client):
        self.supabase = supabase


    async def login_local(self, credentials: CredentialsEntity):
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": credentials.email,
                "password": credentials.password
            })
            return AuthResultEntity(
                user=UserEntity(
                    id=response.user.id,
                    email=response.user.email,
                ),
                tokens=TokensEntity(
                    access_token=response.session.access_token,
                    refresh_token=response.session.refresh_token
                )
            )
        except Exception as e:
            logger.error(e)
            return None


    async def register_local(self, credentials: CredentialsEntity):
        try:
            response = self.supabase.auth.sign_up({
                "email": credentials.email,
                "password": credentials.password
            })
            return AuthResultEntity(
                user=UserEntity(
                    id=response.user.id,
                    email=response.user.email,
                ),
                tokens=TokensEntity(
                    access_token=response.session.access_token,
                    refresh_token=response.session.refresh_token
                )
            )
        except Exception as e:
            logger.error(e)
            return None


    async def sign_in_with_oauth_provider(self, payload: OAuthInputEntity):
        try:
            response = self.supabase.auth.sign_in_with_oauth({
                "provider": payload.provider,
                "options": {
                    "redirect_to": payload.redirect_to,
                }
            })
            logger.info(response)
            return OAuthResponseEntity(
                provider=payload.provider,
                url=response.url
            )
        except Exception as e:
            logger.error(e)
            return None


    async def validate_code(self, code: str):
        try:
            response = self.supabase.auth.exchange_code_for_session(
                {
                    "auth_code": code,
                }
            )
            return AuthResultEntity(
                user=UserEntity(
                    id=response.user.id,
                    email=response.user.email,
                ),
                tokens=TokensEntity(
                    access_token=response.session.access_token,
                    refresh_token=response.session.refresh_token
                )
            )
        except Exception as e:
            logger.error(e)
            return None


    async def refresh_session(self, refresh_token: str):
        try:
            response = self.supabase.auth.refresh_session(refresh_token)
            return AuthResultEntity(
                user=UserEntity(
                    id=response.user.id,
                    email=response.user.email,
                ),
                tokens=TokensEntity(
                    access_token=response.session.access_token,
                    refresh_token=response.session.refresh_token
                )
            )
        except Exception as e:
            logger.error(e)
            return None


    async def validate_session(self, access_token: str):
        try:
            response = self.supabase.auth.get_user(access_token)
            return UserEntity(
                id=response.user.id,
                email=response.user.email,
            )
        except Exception as e:
            logger.error(e)
            return None