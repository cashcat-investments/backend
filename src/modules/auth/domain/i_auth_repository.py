from abc import ABC, abstractmethod
from typing import Optional
from src.modules.auth.domain.auth_entities import UserAndTokensResponse, User

class IAuthRepository(ABC):
    @abstractmethod
    async def login_local(self, email: str, password: str) -> Optional[UserAndTokensResponse]:
        """
        Login a user with email and password \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if Invalid credentials
        """
        pass

    @abstractmethod
    async def register_local(self, email: str, password: str) -> Optional[UserAndTokensResponse]:
        """
        Register a new user with email and password \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if User already exists
        """
        pass

    @abstractmethod
    async def sign_in_with_oauth_provider(self, redirect_to: str, provider: str) -> Optional[UserAndTokensResponse]:
        """
        Sign in with an OAuth provider \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if failed
        """
        pass

    @abstractmethod
    async def validate_code(self, code: str) -> Optional[UserAndTokensResponse]:
        """
        Validate a code from an OAuth provider \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if failed
        """
        pass

    @abstractmethod
    async def refresh_session(self, refresh_token: str) -> Optional[UserAndTokensResponse]:
        """
        Refresh a session \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if refresh token is expired or invalid
        """
        pass

    @abstractmethod
    async def validate_session(self, access_token: str) -> Optional[User]:
        """
        Validate a session \n
        Returns a `User` if successful, \n
        Returns `None` if session is invalid
        """
        pass