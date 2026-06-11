from pydantic import BaseModel

class UserCreate(BaseModel):
    """Pydantic Model
    Used to define action "user creation".
    """
    username: str
    password: str

class UserLogin(BaseModel):
    """Pydantic Model
    Used to define action "user login".
    """
    username: str
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
    password_hash: str
    is_admin: bool = False