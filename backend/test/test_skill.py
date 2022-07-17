import pytest
from httpx import AsyncClient

from main import app
from test.data.user_auth_data import *
from test.data.skill_data import *
from test.common import *

pytest_plugins = ("pytest_asyncio",)


# ----------------------Create skill----------------------
@pytest.mark.asyncio
async def test_create_skill():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/skill/create", json=SKILL_VALID_DATA, headers=headers
        )
    assert response.status_code == 200
    result = response.json()
    assert "key" in result
    assert result["key"] is not None


# ----------------------All skills----------------------
@pytest.mark.asyncio
async def test_get_all_skills():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/skill/all")

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result


# ----------------------Add skill to me----------------------
@pytest.mark.asyncio
async def test_add_no_exist_skill():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/skill/add/to_myself?skill_key={NO_EXIST_SKILL_KEY}", headers=headers
        )
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Skill not found"


@pytest.mark.asyncio
async def test_add_remove_exist_skill():
    headers_admin = await get_header(ADMIN_TEST_AUTH)
    headers_user = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/skill/create", json=SKILL_VALID_DATA, headers=headers_admin
        )
        skill_key = response.json()["key"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/skill/add/to_myself?skill_key={skill_key}", headers=headers_user
        )

    assert response.status_code == 200
    result = response.json()
    assert "key" in result
    assert result["key"] == skill_key

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/skill/remove/at_yorself?skill_key={skill_key}", headers=headers_user
        )

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 0


@pytest.mark.asyncio
async def test_add_already_exist_skill():
    headers_admin = await get_header(ADMIN_TEST_AUTH)
    headers_user = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/skill/create", json=SKILL_VALID_DATA, headers=headers_admin
        )
        skill_key = response.json()["key"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/skill/add/to_myself?skill_key={skill_key}", headers=headers_user
        )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/skill/add/to_myself?skill_key={skill_key}", headers=headers_user
        )

    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Skill already exists"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/skill/remove/at_yorself?skill_key={skill_key}", headers=headers_user
        )

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 0

# ----------------------Delete skill to me----------------------
@pytest.mark.asyncio
async def test_remove_no_exist_skill():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/skill/remove/at_yorself?skill_key={NO_EXIST_SKILL_KEY}", headers=headers
        )
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Skill not found"