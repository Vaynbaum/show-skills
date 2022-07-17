from httpx import AsyncClient

from main import app


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


async def create_event(event, user):
    headers = await get_header(user)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/event/create", json=event, headers=headers)
        event_key = response.json()["key"]
    return event_key


async def arrange_subscription(username, user):
    headers = await get_header(user)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}",
            headers=headers,
        )
    return response

async def annul_subscription(username,user):
    headers = await get_header(user)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/subscription/annul?username_favorite={username}",
            headers=headers,
        )
    return response

async def delete_event(event_key,user):
    headers = await get_header(user)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/event/delete?key={event_key}", headers=headers
        )
    return response
    