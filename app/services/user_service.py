# from typing import Optional
# from sqlalchemy import select, or_
# from datetime import datetime, UTC
# from app.errors.UserErrors import (
#     UserNotFounded,
#     UserAlreadyExists,
#     WrongPasswordError,
#     AccessTokenExpired,
#     AccessTokenMismatch
# )
# from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
# from app.database.models.user import User as UserModel
# from app.database.connection import SessionLocal
# from app.schemas.user import (
#     User,
#     UserCreate,
#     UserLogin,
#     UserResponse,
#     TokenResponse
# )

# def create_user_service(user_data: UserCreate) -> TokenResponse:
#     db = SessionLocal() # initialize db

#     try:
#         # verify if user_data.username/user_data.email already exists
#         existing_user = db.scalar(
#             select(UserModel).where(
#                 or_(
#                     UserModel.username == user_data.username,
#                     UserModel.email == user_data.email
#                 )
#             )
#         )

#         if existing_user:
#             raise UserAlreadyExists(
#                 "Username or email is already taken"
#             )
        
#         new_user = UserModel(
#             username=user_data.username,
#             email=user_data.email,
#             password_hash=get_password_hash(user_data.password),
#         )

#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
        

#         token = create_access_token({
#             "sub": str(new_user.id)
#             }
#         )

#         return TokenResponse(access_token=token)
#     finally:
#         db.close()



# def login_user_service(user_data: UserLogin) -> TokenResponse:
#     db = SessionLocal() # init db
#     try:
#         # verify if user_data.username_or_email is in table
#         existing_user = db.scalar(
#             select(UserModel).where(
#                 or_(
#                     UserModel.username==user_data.username_or_email,
#                     UserModel.email==user_data.username_or_email,
#                 )
#             )
#         )

#         if not existing_user:
#             raise UserNotFounded(
#                 "Invalid credentials"
#             )
        
#         if not verify_password(
#             user_data.password,
#             existing_user.password_hash
#         ):
#             raise WrongPasswordError(
#                 "Invalid credentials"
#             )
        
#         token = create_access_token({
#             "sub": str(existing_user.id)
#         })


#         return TokenResponse(access_token=token)
#     finally:
#         db.close()


 
# def get_current_user(token: TokenResponse) -> User:
#     db = SessionLocal()
#     try:
#         decoded_token: dict = decode_access_token(token)

#         if not decoded_token: # if func output is "{}", then something went wrong and we got a mismatch
#             raise AccessTokenMismatch(
#                 "JWT Token mismatched"
#             )

#         # for now, I'll not apply expire for tokens...
#         if decoded_token["exp"] >= datetime.now(UTC): pass # just applying the logical interrupt

        
#         # now, select the current user based on sub.
#         user_db_model = db.scalar(
#             select(UserModel).where(
#                 UserModel.id==decoded_token["sub"]
#             )
#         )

#         user_schema = User(
#             id=user_db_model.id,
#             username=user_db_model.username,
#             email=user_db_model.email,
#             is_admin=user_db_model.is_admin
#         )

#         return user_schema
#     finally:
#         db.close()




# Serviço de Usuários
# Objetivo do arquivo:
# Permitir a criação de novos usuários
# Permitir a entrada de usuários
# Permitir que usuários não precisem efetuar login repetidamente nem adicionar informações sensiveis à URL final.

# INTERNAL LIBS IMPORTS
from typing import Dict
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

# USER RELATED IMPORTS
from app.schemas.user import *
from app.errors.UserErrors import *
# OTHER IMPORTS
from app.database.dependencies import get_db
from app.database.models.user import User as UserModel
from app.core.security import (
    get_password_hash as hash_password,
    verify_password,
    create_access_token as create_token,
    decode_access_token as decode_token
)

# from "root/app/database/dependencies"
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close() 

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)
  
def get_user_by_id(
        session: Session,
        user_id: int
) -> UserModel:
    user: UserModel = session.scalar(
        select(UserModel).where(
            UserModel.id==user_id
        )
    )

    if not user:
        raise UserNotFounded()
    
    return user

def get_user_by_name(
        session: Session,
        username: str
) -> UserModel:
    user: UserModel = session.scalar(
        select(UserModel).where(
            UserModel.username==username
        )
    )

    # Global handlers already handles all errors types
    if not user:
        raise UserNotFounded()
    
    return user

def get_user_by_email(
        session: Session,
        email: str
) -> UserModel:
    user: UserModel = session.scalar(
        select(UserModel).where(
            UserModel.email==email
        )
    )

    if not user:
        raise UserNotFounded()
    
    return user

def get_user_by_username_or_email(db: Session, username: str, email: str) -> UserModel:
    return db.scalar(select(UserModel).where(or_(
        UserModel.username==username,
        UserModel.email==email
    )))


def model_to_schema_user(user: UserModel) -> User:
    return User(
        id=user.id,
        username=user.username,
        email=user.email,
        is_admin=user.is_admin
    )

def create_user_service(db:Session, info: UserCreate) -> TokenResponse:
    if get_user_by_username_or_email(db, info.username, info.email):
        raise UserAlreadyExists()
    
    hashed_password: str = hash_password(info.password)

    user: UserModel = UserModel(
        username=info.username,
        email=info.email,
        password_hash=hashed_password
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        db.rollback()
        raise

    access_token: str = create_token({
        "sub": str(user.id)
    })

    return TokenResponse(
        access_token=access_token
    )


def login_user_service(db: Session, identifier: str, password: str) -> TokenResponse:
    if not (logged_user:=get_user_by_username_or_email(db=db, username=identifier, email=identifier)):
        raise InvalidCredentials()
    
    
    if not verify_password(password, logged_user.password_hash):
        raise WrongPasswordError()
    

    
    access_token: str = create_token({
        "sub": str(logged_user.id)
    })

    return TokenResponse(
        access_token=access_token
    )

def get_cur_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    decoded_token: Dict = decode_token(token)
    if not decoded_token:
        raise AccessTokenMismatch()

    user_id: int = int(decoded_token["sub"])
    model_user = get_user_by_id(db, user_id=user_id)
    return model_to_schema_user(model_user)