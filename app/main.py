# ROOT ROUTE
# "docapi/"
# derivatives from: "app/api/..." 
# File create on 6/11/2026 with One author.

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.database.init_db import init_db
from app.api.routes.users import user_router

app: FastAPI = FastAPI()

app.include_router(user_router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def home():
    return {"log": "started"}

