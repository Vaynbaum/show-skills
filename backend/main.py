import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from routes import (
    auth_router,
    comment_router,
    like_router,
    post_router,
    role_router,
    skill_router,
    suggestion_router,
    user_router,
    subscription_router,
    link_router,
    event_router,
)


load_dotenv()
app = FastAPI(
    title=os.getenv("PROJECT_NAME"),
    description="SkillShow API 👩‍🏭",
    contact={
        "name": "skill-show",
        "email": "mr.vaynbaum@mail.ru",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth")
app.include_router(user_router.router, prefix="/user")
app.include_router(skill_router.router, prefix="/skill")
app.include_router(link_router.router, prefix="/link")
app.include_router(event_router.router, prefix="/event")
app.include_router(subscription_router.router, prefix="/subscription")
app.include_router(role_router.router, prefix="/role")
app.include_router(post_router.router, prefix="/post")
app.include_router(like_router.router, prefix="/like")
app.include_router(comment_router.router, prefix="/comment")
app.include_router(suggestion_router.router, prefix="/suggestion")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
