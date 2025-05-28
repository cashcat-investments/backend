from typing import Optional
from pydantic import BaseModel

class UserEntity(BaseModel):
    id: str
    email: str

class UserProfileEntity(UserEntity):
    first_name: str
    last_name: str
    profile_pic: Optional[str] = None