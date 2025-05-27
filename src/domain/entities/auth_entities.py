class UserAuthEntity():
    id: str
    email: str

class TokensEntity():
    access_token: str
    refresh_token: str

class AuthResultEntity():
    user: UserAuthEntity
    tokens: TokensEntity

class LoginInputEntity():
    email: str
    password: str

class RegisterInputEntity():
    email: str
    password: str

class OAuthInputEntity():
    redirect_to: str
    provider: str

class OAuthResponseEntity():
    provider: str
    url: str