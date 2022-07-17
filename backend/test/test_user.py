import pytest
from httpx import AsyncClient

from main import app
from test.data.user_auth_data import *
from test.data.user_data import *
from test.common import *

pytest_plugins = ("pytest_asyncio",)


# ----------------------All users----------------------
@pytest.mark.asyncio
async def test_all_users_no_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/all")
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_all_users_no_rights_token_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json=USER_TEST_AUTH)
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.get("/user/all", headers=headers)
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )


@pytest.mark.asyncio
async def test_all_users_have_rights_token_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/all", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert result["items"] is not None
    assert result["count"] > 0


@pytest.mark.asyncio
async def test_all_users_have_rights_token_super_admin_count_1():
    headers = await get_header(SUPER_ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/user/all?limit=1",
            headers=headers,
        )
    assert response.status_code == 200
    result = response.json()
    assert "count" in result
    assert result["count"] == 1


# ----------------------By username----------------------
@pytest.mark.asyncio
async def test_user_by_exist_username():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/user/profile/{USER_TEST_USERNAME}",
        )
    assert response.status_code == 200
    result = response.json()
    assert "username" in result
    assert result["username"] == USER_TEST_USERNAME
    assert "key" in result
    assert result["key"] is not None


@pytest.mark.asyncio
async def test_user_by_no_exist_username():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/user/profile/{NO_EXIST_USERNAME}",
        )
    assert response.status_code == 200
    assert response.json() == None


# ----------------------Delete----------------------
@pytest.mark.asyncio
async def test_delete_user_by_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    username = REGISTRATION_ACCOUNT_TO_DELETE["username"]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/signup",
            json=REGISTRATION_ACCOUNT_TO_DELETE,
        )
        response = await ac.get(
            f"/user/profile/{username}",
        )
        user_key = response.json()["key"]

        response = await ac.delete(f"/user/?key={user_key}", headers=headers)
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "There is no access to this method"

    await delete_auth(REGISTRATION_ACCOUNT_TO_DELETE)


@pytest.mark.asyncio
async def test_delete_user_by_super_admin():
    headers = await get_header(SUPER_ADMIN_TEST_AUTH)
    username = REGISTRATION_ACCOUNT_TO_DELETE["username"]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/signup",
            json=REGISTRATION_ACCOUNT_TO_DELETE,
        )
        response = await ac.get(
            f"/user/profile/{username}",
        )
        user_key = response.json()["key"]

        response = await ac.delete(f"/user/?key={user_key}", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Deletion successful"


@pytest.mark.asyncio
async def test_delete_user_by_user():
    username = REGISTRATION_ACCOUNT_TO_DELETE["username"]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/signup",
            json=REGISTRATION_ACCOUNT_TO_DELETE,
        )
        headers = await get_header(ACCOUNT_TO_DELETE_AUTH)
        response = await ac.get(
            f"/user/profile/{username}",
        )
        user_key = response.json()["key"]

        response = await ac.delete(f"/user/?key={user_key}", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Deletion successful"


@pytest.mark.asyncio
async def test_delete_user_by_no_exist_key():
    headers = await get_header(SUPER_ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/user/?key={NO_EXIST_KEY_USER}", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Deletion successful"


@pytest.mark.asyncio
async def test_delete_user_by_other_user():
    headers = await get_header(USER_TEST_AUTH)
    username = REGISTRATION_ACCOUNT_TO_DELETE["username"]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/signup",
            json=REGISTRATION_ACCOUNT_TO_DELETE,
        )
        response = await ac.get(
            f"/user/profile/{username}",
        )
        user_key = response.json()["key"]

        response = await ac.delete(f"/user/?key={user_key}", headers=headers)
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "There is no access to this method"

    await delete_auth(REGISTRATION_ACCOUNT_TO_DELETE)


# ----------------------Update----------------------
@pytest.mark.asyncio
async def test_update_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = await get_header(USER_TEST_AUTH)
        response = await ac.put(
            f"/user/additional_data",
            headers=headers,
            json=ADDITIONAL_VALID_DATA,
        )
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Data successfully added"
    
@pytest.mark.asyncio
async def test_update_user_invalid_year():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            f"/user/additional_data",
            headers=headers,
            json=ADDITIONAL_INVALID_DATA,
        )
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Invalid year"
