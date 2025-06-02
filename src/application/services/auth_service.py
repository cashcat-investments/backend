from src.domain.repositories.i_auth_repository import IAuthRepository
from typing import Optional
from src.application.dtos.auth_dtos import AuthResponse, SignUpRequest
from src.domain.entities.auth_entities import CredentialsEntity, AuthResultEntity, OAuthResponseEntity, OAuthInputEntity
from src.domain.entities.user_entities import UserEntity, UserProfileEntity
from src.domain.repositories.i_user_repository import IUserRepository

class AuthService:
    def __init__(self, auth_repository: IAuthRepository, user_repository: IUserRepository):
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    async def login_local(self, credentials: CredentialsEntity) -> Optional[AuthResponse]:
        result: Optional[AuthResultEntity] = await self.auth_repository.login_local(credentials=credentials)

        if result is None:
            return None
        
        # TODO: Use user_repository to get  the user
        # user = await self.user_repository.get_user(result.user)

        user_profile = UserProfileEntity(
            id=result.user.id,
            email=result.user.email,
            first_name="John",
            last_name="Doe",
            profile_pic=None
        )

        return AuthResponse(user=user_profile, tokens=result.tokens)

    async def register_local(self, payload: SignUpRequest) -> Optional[AuthResponse]:
        credentials = CredentialsEntity(email=payload.email, password=payload.password)
        result: Optional[AuthResultEntity] = await self.auth_repository.register_local(credentials=credentials)
        if result is None:
            return None

        user_profile = self.user_repository.add(
            id=result.user.id,
            email=result.user.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            profile_pic=None
        )
        
        return AuthResponse(user=user_profile, tokens=result.tokens)


    async def sign_in_with_google(self, redirect_to: str) -> Optional[OAuthResponseEntity]:
        payload = OAuthInputEntity(
            redirect_to=redirect_to,
            provider="google"
        )
        return await self.auth_repository.sign_in_with_oauth_provider(payload)

    async def validate_code(self, code: str) -> Optional[AuthResponse]:
        result: Optional[AuthResultEntity] = await self.auth_repository.validate_code(code)
        if result is None:
            return None
        
        # TODO: Use user_repository to get or create the user
        # user = await self.user_repository.get_or_create_user(result.user)
        
        user_profile = UserProfileEntity(
            id=result.user.id,
            email=result.user.email,
            first_name="John",
            last_name="Doe",
            profile_pic=None
        )

        return AuthResponse(user=user_profile, tokens=result.tokens)

    async def refresh_session(self, refresh_token: str) -> Optional[AuthResponse]:
        return await self.auth_repository.refresh_session(refresh_token)

    async def validate_session(self, access_token: str) -> Optional[UserProfileEntity]:
        result: Optional[UserEntity] = await self.auth_repository.validate_session(access_token)
        if result is None:
            return None

        # TODO: Use user_repository to get  the user
        # user = await self.user_repository.get_user(result.user)

        return UserProfileEntity(
            id=result.id,
            email=result.email,
            first_name="John",
            last_name="Doe",
            profile_pic=None
        )
