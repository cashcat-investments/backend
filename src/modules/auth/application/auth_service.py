from src.modules.auth.domain.i_auth_repository import IAuthRepository
from typing import Optional
from src.modules.auth.domain.auth_entities import UserAndTokensResponse, User

class AuthService:
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository

    async def login_local(self, email: str, password: str) -> Optional[UserAndTokensResponse]:
        return await self.auth_repository.login_local(email, password)

    async def register_local(self, email: str, password: str) -> Optional[UserAndTokensResponse]:
        return await self.auth_repository.register_local(email, password)

    async def sign_in_with_google(self, redirect_to: str) -> Optional[UserAndTokensResponse]:
        return await self.auth_repository.sign_in_with_oauth_provider(redirect_to, "google")
    
    async def validate_code(self, code: str) -> Optional[UserAndTokensResponse]:
        return await self.auth_repository.validate_code(code)
    
    async def refresh_session(self, refresh_token: str) -> Optional[UserAndTokensResponse]:
        return await self.auth_repository.refresh_session(refresh_token)
    
    async def validate_session(self, access_token: str) -> Optional[User]:
        return await self.auth_repository.validate_session(access_token)
