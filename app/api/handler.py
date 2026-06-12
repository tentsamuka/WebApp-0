from fastapi.responses import JSONResponse
from app.main import app
from app.errors.UserErrors import (
    UserAlreadyExists,
    UserNotFounded,
    WrongPasswordError
)

@app.exception_handler(UserAlreadyExists)
async def user_exists_handler(request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )

@app.exception_handler(UserNotFounded)
async def user_not_found_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )

@app.exception_handler(WrongPasswordError)
async def wrong_password_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )