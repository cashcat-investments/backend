from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.auth_entities import AuthResultEntity, OAuthInputEntity, OAuthResponseEntity, CredentialsEntity
from src.domain.entities.user_entities import UserEntity

class IAuthRepository(ABC):
    @abstractmethod
    async def login_local(self, credentials: CredentialsEntity) -> Optional[AuthResultEntity]:
        """
        Login a user with email and password \n
        Receives a `CredentialsEntity` \n
        Returns a `AuthResultEntity` if successful, \n
        Returns `None` if Invalid credentials
        """
        pass

    @abstractmethod
    async def register_local(self, credentials: CredentialsEntity) -> Optional[AuthResultEntity]:
        """
        Register a new user with email and password \n
        Receives a `CredentialsEntity` \n
        Returns a `AuthResultEntity` if successful, \n
        Returns `None` if User already exists
        """
        pass

    @abstractmethod
    async def sign_in_with_oauth_provider(self, payload: OAuthInputEntity) -> Optional[OAuthResponseEntity]:
        """
        Sign in with an OAuth provider \n
        Returns a `OAuthResponseEntity` if successful, \n
        Returns `None` if failed
        """
        pass

    @abstractmethod
    async def validate_code(self, code: str) -> Optional[AuthResultEntity]:
        """
        Validate a code from an OAuth provider \n
        Returns a `AuthResultEntity` if successful, \n
        Returns `None` if failed
        """
        pass

    @abstractmethod
    async def refresh_session(self, refresh_token: str) -> Optional[AuthResultEntity]:
        """
        Refresh a session \n
        Returns a `AuthResultEntity` if successful, \n
        Returns `None` if refresh token is expired or invalid
        """
        pass

    @abstractmethod
    async def validate_session(self, access_token: str) -> Optional[UserEntity]:
        """
        Validate a session \n
        Returns a `User` if successful, \n
        Returns `None` if session is invalid
        """
        pass