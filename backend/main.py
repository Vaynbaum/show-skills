import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from routes import auth_router, user_router

app = FastAPI(title=os.getenv("PROJECT_NAME"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix='/auth')
app.include_router(user_router.router, prefix='/user')
