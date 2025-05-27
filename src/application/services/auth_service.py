from domain.repositories.i_auth_repository import IAuthRepository
from typing import Optional
from domain.entities.auth_entities import AuthResultEntity, UserAuthEntity, LoginInputEntity, RegisterInputEntity, OAuthInputEntity, OAuthResponseEntity

class AuthService:
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository

    async def login_local(self, payload: LoginInputEntity) -> Optional[AuthResultEntity]:
        return await self.auth_repository.login_local(payload)

    async def register_local(self, payload: RegisterInputEntity) -> Optional[AuthResultEntity]:
        return await self.auth_repository.register_local(payload)

    async def sign_in_with_google(self, redirect_to: str) -> Optional[OAuthResponseEntity]:
        payload = OAuthInputEntity(redirect_to=redirect_to, provider="google")
        return await self.auth_repository.sign_in_with_oauth_provider(payload)
    
    async def validate_code(self, code: str) -> Optional[AuthResultEntity]:
        return await self.auth_repository.validate_code(code)
    
    async def refresh_session(self, refresh_token: str) -> Optional[AuthResultEntity]:
        return await self.auth_repository.refresh_session(refresh_token)
    
    async def validate_session(self, access_token: str) -> Optional[UserAuthEntity]:
        return await self.auth_repository.validate_session(access_token)
