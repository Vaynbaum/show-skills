import pytest
from httpx import AsyncClient

from main import app
from test.common import *
from test.data.comment_data import *
from test.data.user_auth_data import *

pytest_plugins = ("pytest_asyncio",)

# ----------------------Add comment----------------------
@pytest.mark.asyncio
async def test_add_comment_to_no_exist_post():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/comment/?post_key={NO_EXIST_POST_KEY}",
            json=COMMENT_DATA,
            headers=headers,
        )
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_add_remove_comment_to_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SOBOLEV_REGISTRATION_VALID_DATA)
        headers = await get_header(SOBOLEV_AUTH_VALID_DATA)

        response = await ac.post("/post/create", json=POST_DATA, headers=headers)
        post_key = response.json()["key"]

        response = await ac.post(
            f"/comment/?post_key={post_key}",
            json=COMMENT_DATA,
            headers=headers,
        )

    assert response.status_code == 200
    result = response.json()
    assert "key" in result
    assert result["key"] is not None
    comment_key = result["key"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/comment/?post_key={post_key}&comment_key={comment_key}", headers=headers
        )

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 0

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/post/?post_key={post_key}", headers=headers)
    await delete_auth(SOBOLEV_REGISTRATION_VALID_DATA)


# ----------------------Delete comment----------------------
@pytest.mark.asyncio
async def test_delete_comment_to_post_admin():
    headers_admin = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SOBOLEV_REGISTRATION_VALID_DATA)
        headers = await get_header(SOBOLEV_AUTH_VALID_DATA)

        response = await ac.post("/post/create", json=POST_DATA, headers=headers)
        post_key = response.json()["key"]

        response = await ac.post(
            f"/comment/?post_key={post_key}",
            json=COMMENT_DATA,
            headers=headers,
        )
        comment_key = response.json()["key"]

        response = await ac.delete(
            f"/comment/?post_key={post_key}&comment_key={comment_key}",
            headers=headers_admin,
        )

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 0

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/post/?post_key={post_key}", headers=headers)
    await delete_auth(SOBOLEV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_delete_no_exist_comment():
    headers_admin = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SOBOLEV_REGISTRATION_VALID_DATA)
        headers = await get_header(SOBOLEV_AUTH_VALID_DATA)

        response = await ac.post("/post/create", json=POST_DATA, headers=headers)
        post_key = response.json()["key"]

        response = await ac.delete(
            f"/comment/?post_key={post_key}&comment_key={NO_EXIST_COMMENT_KEY}",
            headers=headers_admin,
        )

    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Comment not found"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/post/?post_key={post_key}", headers=headers)
    await delete_auth(SOBOLEV_REGISTRATION_VALID_DATA)

@pytest.mark.asyncio
async def test_delete_no_exist_comment_to_no_exist_post():
    headers_admin = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/comment/?post_key={NO_EXIST_POST_KEY}&comment_key={NO_EXIST_COMMENT_KEY}",
            headers=headers_admin,
        )

    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Post not found"