import pytest
from httpx import AsyncClient

from main import app
from .data.auth_data import *
from .data.user_auth_data import *

pytest_plugins = ("pytest_asyncio",)


async def get_header(user):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json=user)
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
    return headers


async def delete_auth(user):
    username = user["username"]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = await get_header(
            {"email": user["email"], "password": user["password"]}
        )
        response = await ac.get(
            f"/user/profile/{username}",
        )
        user_key = response.json()["key"]
        response = await ac.delete(f"/user/?key={user_key}", headers=headers)
    return response
