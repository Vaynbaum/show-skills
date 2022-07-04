import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv

from routes import auth_router, skill_router, user_router, subscription_router

load_dotenv()
app = FastAPI(title=os.getenv("PROJECT_NAME"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth")
app.include_router(user_router.router, prefix="/user")
app.include_router(skill_router.router, prefix="/skill")
app.include_router(subscription_router.router, prefix="/subscription")