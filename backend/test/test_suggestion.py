import pytest
from httpx import AsyncClient

from main import app
from test.common import *
from test.data.suggestion_data import *
from test.data.user_auth_data import *

pytest_plugins = ("pytest_asyncio",)

# ----------------------Post Suggestion----------------------
@pytest.mark.asyncio
async def test_create_suggestion_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/suggestion/", json=SUGGESTION_DATA, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "key" in result
    assert result["key"] is not None


@pytest.mark.asyncio
async def test_create_suggestion_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/suggestion/", json=SUGGESTION_DATA, headers=headers)
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )


# ----------------------All Suggestions----------------------
@pytest.mark.asyncio
async def test_get_suggestions_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/suggestion/", headers=headers)
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )


@pytest.mark.asyncio
async def test_get_suggestions_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/suggestion/", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result


# ----------------------Tick Suggestion----------------------
@pytest.mark.asyncio
async def test_tick_suggestion_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/suggestion/", json=SUGGESTION_DATA, headers=headers)
        suggestion_key = response.json()["key"] is not None

        response = await ac.put(
            f"/suggestion/tick?suggestion_key={suggestion_key}",
            json=SUGGESTION_DATA_TICK,
            headers=headers,
        )
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )
    
@pytest.mark.asyncio
async def test_tick_suggestion_admin():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/suggestion/", json=SUGGESTION_DATA, headers=headers)
        suggestion_key = response.json()["key"]
        headers = await get_header(ADMIN_TEST_AUTH)
        response = await ac.put(
            f"/suggestion/tick?suggestion_key={suggestion_key}",
            json=SUGGESTION_DATA_TICK,
            headers=headers,
        )
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert (
        result["message"] == "Ticking  successful"
    )