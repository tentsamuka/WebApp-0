from fastapi import APIRouter, HTTPException

from app.errors.UserErrors import (
    UserAlreadyExists,
    UserNotFounded,
    WrongPasswordError
    )

from app.schemas.user import (
    User,  
    UserCreate, 
    UserLogin, 
    UserResponse
    )

from app.services.user_service import (
    create_user_service, 
    login_user_service, 
    )

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post(
    "/register",
    response_model=UserResponse
)
async def register(user: UserCreate):
    return create_user_service(user)


@user_router.post(
    "/login",
    response_model=UserResponse
)
async def login(user: UserLogin):
    return login_user_service(user)

