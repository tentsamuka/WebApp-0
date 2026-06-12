from typing import Union
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """Pydantic Model
    Used to define action "user creation".
    """
    username: str
    email: EmailStr 
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    """Pydantic Model
    Used to define action "user login".
    """
    username_or_email: Union[str, EmailStr]
    password: str

class UserResponse(BaseModel):
    """Pydantic Model
    Used to define action "user reponse".
    """
    id: int
    username: str
    is_admin: bool = False

class User(BaseModel):
    """Pydantic Model
    Used to define an User.
    """
    id: int
    username: str
    email: EmailStr
    is_admin: bool = False