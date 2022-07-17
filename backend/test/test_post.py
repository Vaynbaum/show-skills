import pytest
from httpx import AsyncClient

from main import app
from test.common import *
from test.data.post_data import *
from test.data.user_auth_data import *

pytest_plugins = ("pytest_asyncio",)

# ----------------------Create post----------------------
@pytest.mark.asyncio
async def test_create_delete_post():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/post/create", json=POST_DATA, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "key" in result
    assert result["key"] is not None
    post_key = result["key"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/post/?post_key={post_key}", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Deletion successful"


# ----------------------Delete post----------------------
@pytest.mark.asyncio
async def test_delete_no_exist_post():
    headers = await get_header(USER_TEST_AUTH)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/post/?post_key={NO_EXIST_POST_KEY}", headers=headers
        )
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_delete_post_other_user():
    headers_user = await get_header(USER_TEST_AUTH)
    headers_admin = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SMIRNOV_REGISTRATION_VALID_DATA)
        headers_smirnov = await get_header(SMIRNOV_AUTH_VALID_DATA)
        response = await ac.post(
            "/post/create", json=POST_DATA, headers=headers_smirnov
        )
        post_key = response.json()["key"]
        response = await ac.delete(f"/post/?post_key={post_key}", headers=headers_user)

    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "There is no access to this method"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/post/?post_key={post_key}", headers=headers_admin)
    await delete_auth(SMIRNOV_REGISTRATION_VALID_DATA)


# ----------------------Get all posts----------------------
@pytest.mark.asyncio
async def test_get_all_posts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SMIRNOV_REGISTRATION_VALID_DATA)
        response = await ac.get("/post/all")

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert result["count"] == 0

    headers_smirnov = await get_header(SMIRNOV_AUTH_VALID_DATA)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/post/create", json=POST_DATA, headers=headers_smirnov
        )
        post_key = response.json()["key"]
        response = await ac.get("/post/all")
    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert result["count"] > 0

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/post/?post_key={post_key}", headers=headers_smirnov
        )
    await delete_auth(SMIRNOV_REGISTRATION_VALID_DATA)


# ----------------------Get posts by skill----------------------
@pytest.mark.asyncio
async def test_get_posts_by_no_exist_skill():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/post/by_skill?name_skill={NO_EXIST_SKILL_NAME}")

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert result["count"] == 0


@pytest.mark.asyncio
async def test_get_posts_by_skill_name():
    headers = await get_header(USER_TEST_AUTH)
    name_skill = POST_DATA["skill"]["name"]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/post/by_skill?name_skill={name_skill}")

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert result["count"] == 0

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/post/create", json=POST_DATA, headers=headers)
        post_key = response.json()["key"]
        response = await ac.get(f"/post/by_skill?name_skill={name_skill}")

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert result["count"] == 1

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/post/?post_key={post_key}", headers=headers)


# ----------------------Edit post----------------------
@pytest.mark.asyncio
async def test_edit_no_exist_post():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            f"/post/?post_key={NO_EXIST_POST_KEY}", json=POST_EDIT_DATA, headers=headers
        )

    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == 'Post not found'


@pytest.mark.asyncio
async def test_edit_post_other_user():
    headers_user = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SMIRNOV_REGISTRATION_VALID_DATA)
        headers_smirnov = await get_header(SMIRNOV_AUTH_VALID_DATA)

        response = await ac.post(
            "/post/create", json=POST_DATA, headers=headers_smirnov
        )
        post_key = response.json()["key"]
        
        response = await ac.put(
            f"/post/?post_key={post_key}",
            json=POST_EDIT_DATA,
            headers=headers_user,
        )

    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "There is no access to this method"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/post/?post_key={post_key}", headers=headers_smirnov
        )
    await delete_auth(SMIRNOV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_edit_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SMIRNOV_REGISTRATION_VALID_DATA)
        headers_smirnov = await get_header(SMIRNOV_AUTH_VALID_DATA)

        response = await ac.post(
            "/post/create", json=POST_DATA, headers=headers_smirnov
        )
        post_key = response.json()["key"]
        
        response = await ac.put(
            f"/post/?post_key={post_key}",
            json=POST_EDIT_DATA,
            headers=headers_smirnov,
        )

    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Editing successful"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/post/?post_key={post_key}", headers=headers_smirnov
        )
    await delete_auth(SMIRNOV_REGISTRATION_VALID_DATA)
