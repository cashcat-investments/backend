from pydantic import BaseModel

class LocalLoginRequest(BaseModel):
    email: str
    password: str

class LocalRegisterRequest(BaseModel):
    email: str
    password: str