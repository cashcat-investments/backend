from src.auth.models import LocalLoginRequest, LocalRegisterRequest
from src.auth.repositories import AuthRepository

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def login(self, request: LocalLoginRequest):
        return await self.auth_repository.login(request)

    async def register(self, request: LocalRegisterRequest):
        return await self.auth_repository.register(request)

    async def sign_in_with_google(self, redirect_to: str):
        return await self.auth_repository.sign_in_with_google(redirect_to)
    
    async def validate_google_code(self, code: str):
        return await self.auth_repository.validate_google_code(code)
    
    async def refresh_session(self, refresh_token: str):
        return await self.auth_repository.refresh_session(refresh_token)
    
    async def validate_session(self, access_token: str):
        return await self.auth_repository.validate_session(access_token)
