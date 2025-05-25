from src.auth.models import LocalLoginRequest, UserAndTokensResponse, User, LocalRegisterRequest
from src.utils.supabase import Supabase
from src.utils.logger import setup_logger

logger = setup_logger("AuthRepository")

class AuthRepository:
    def __init__(self, supabase: Supabase):
        self.supabase = supabase.get_client()

    async def login(self, request: LocalLoginRequest):
        """
        Login a user with email and password \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if Invalid credentials
        """
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": request.email,
                "password": request.password
            })
            return UserAndTokensResponse(
                user=User(
                    id=response.user.id,
                    email=response.user.email,
                    role=response.user.role
                ),
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token
            )
        except Exception as e:
            logger.error(e)
            return None


    async def register(self, request: LocalRegisterRequest):
        """
        Register a new user with email and password \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if User already exists
        """

        try:
            response = self.supabase.auth.sign_up({
                "email": request.email,
                "password": request.password
            })
            return UserAndTokensResponse(
                user=User(
                    id=response.user.id,
                    email=response.user.email,
                    role=response.user.role
                ),
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token
            )
        except Exception as e:
            logger.error(e)
            return None
        
    async def sign_in_with_google(self, redirect_to: str):
        """
        Sign in with Google \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if failed
        """
        try:
            response = self.supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirect_to": redirect_to,
                }
            })
            logger.info(response)
            return response
        except Exception as e:
            logger.error(e)
            return None
        
    async def validate_google_code(self, code: str):
        """
        Validate a Google code \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if failed
        """
        try:
            response = self.supabase.auth.exchange_code_for_session(
                {
                    "auth_code": code,
                }
            )
            return UserAndTokensResponse(
                user=User(
                    id=response.user.id,
                    email=response.user.email,
                    role=response.user.role
                ),
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token
            )
        except Exception as e:
            logger.error(e)
            return None

    async def refresh_session(self, refresh_token: str):
        """
        Refresh a session \n
        Returns a `UserAndTokensResponse` if successful, \n
        Returns `None` if refresh token is expired or invalid
        """
        try:
            response = self.supabase.auth.refresh_session(refresh_token)
            return UserAndTokensResponse(
                user=User(
                    id=response.user.id,
                    email=response.user.email,
                    role=response.user.role
                ),
                access_token=response.session.access_token,
                refresh_token=refresh_token
            )
        except Exception as e:
            logger.error(e)
            return None
    
    async def validate_session(self, access_token: str):
        """
        Validate a session \n
        Returns a `User` if successful, \n
        Returns `None` if session is invalid
        """
        try:
            response = self.supabase.auth.get_user(access_token)
            return User(
                id=response.user.id,
                email=response.user.email,
                role=response.user.role
            )
        except Exception as e:
            logger.error(e)
            return None