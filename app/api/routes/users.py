from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database.dependencies import get_db
from app.errors.UserErrors import (
    UserAlreadyExists,
    UserNotFounded,
    WrongPasswordError
    )

from app.schemas.user import (
    User,  
    UserCreate, 
    UserLogin, 
    UserResponse,
    TokenResponse
    )

from app.services.user_service import (
    create_user_service, 
    login_user_service,
    get_cur_user
    )





user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.post("/register")
def register(
    user: UserCreate,
    db = Depends(get_db)
):
    return create_user_service(db, user)

@user_router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_db)
):
    return login_user_service(db, form_data.username, form_data.password)


@user_router.get("/me")
async def me(
    current_user: User = Depends(get_cur_user)
):
    return current_user