from src.domain.entities.user_entities import UserEntity
from pydantic import BaseModel


class CredentialsEntity(BaseModel):
    email: str
    password: str

class TokensEntity(BaseModel):
    access_token: str
    refresh_token: str

class AuthResultEntity(BaseModel):
    user: UserEntity
    tokens: TokensEntity

class OAuthInputEntity(BaseModel):
    redirect_to: str
    provider: str

class OAuthResponseEntity(BaseModel):
    provider: str
    url: str