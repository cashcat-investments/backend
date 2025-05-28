from pydantic import BaseModel
from src.domain.entities.auth_entities import TokensEntity, CredentialsEntity
from src.domain.entities.user_entities import UserProfileEntity

class SignUpRequest(CredentialsEntity):
    first_name: str
    last_name: str

class AuthResponse(BaseModel):
    user: UserProfileEntity
    tokens: TokensEntity