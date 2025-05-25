from pydantic import BaseModel


AUTH_PREFIX = "auth"

class User(BaseModel):
    id: str
    role: str
    email: str

class LocalLoginRequest(BaseModel):
    email: str
    password: str

class UserAndTokensResponse(BaseModel):
    user: User
    access_token: str
    refresh_token: str

class LocalRegisterRequest(BaseModel):
    email: str
    password: str
