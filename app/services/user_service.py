from typing import Optional
from sqlalchemy import select, or_
from app.errors.UserErrors import (
    UserNotFounded,
    UserAlreadyExists,
    WrongPasswordError
)
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.database.models.user import User as UserModel
from app.database.connection import SessionLocal
from app.schemas.user import (
    User,
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse
)

def create_user_service(user_data: UserCreate) -> TokenResponse:
    db = SessionLocal() # initialize db

    try:
        # verify if user_data.username/user_data.email already exists
        existing_user = db.scalar(
            select(UserModel).where(
                or_(
                    UserModel.username == user_data.username,
                    UserModel.email == user_data.email
                )
            )
        )

        if existing_user:
            raise UserAlreadyExists(
                "Username or email is already taken"
            )
        
        new_user = UserModel(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        

        token = create_access_token({
            "sub": str(new_user.id)
            }
        )

        return TokenResponse(access_token=token)
    finally:
        db.close()



def login_user_service(user_data: UserLogin) -> TokenResponse:
    db = SessionLocal() # init db
    try:
        # verify if user_data.username_or_email is in table
        existing_user = db.scalar(
            select(UserModel).where(
                or_(
                    UserModel.username==user_data.username_or_email,
                    UserModel.email==user_data.username_or_email,
                )
            )
        )

        if not existing_user:
            raise UserNotFounded(
                "User was not founded in the database"
            )
        
        if not verify_password(
            user_data.password,
            existing_user.password_hash
        ):
            raise WrongPasswordError(
                "Wrong password provided"
            )
        
        token = create_access_token({
            "sub": str(existing_user.id)
        })


        return TokenResponse(token)
    finally:
        db.close()



 
