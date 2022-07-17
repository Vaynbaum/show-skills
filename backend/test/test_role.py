import pytest
from httpx import AsyncClient

from main import app
from test.common import *
from test.data.role_data import *
from test.data.user_auth_data import *

pytest_plugins = ("pytest_asyncio",)

# ----------------------All roles----------------------
@pytest.mark.asyncio
async def test_get_all_roles_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/role/all_can_assign", headers=headers)
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )


@pytest.mark.asyncio
async def test_get_all_roles_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/role/all_can_assign", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert len(result["items"]) > 0
    assert result["count"] > 0


# ----------------------Assign role----------------------
@pytest.mark.asyncio
async def test_assign_role_to_super_admin_from_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/user/profile/{SUPER_ADMIN_TEST_USERNAME}",
        )
        user_key = response.json()["key"]

        response = await ac.get("/role/all_can_assign", headers=headers)
        roles = response.json()["items"]
        user_role = list(filter(lambda role: "user" == role["name_en"], roles))
        role_key = user_role[0]["key"]

        response = await ac.post(
            f"/role/assign?user_key={user_key}&role_key={role_key}", headers=headers
        )
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "There is no access to this method"


@pytest.mark.asyncio
async def test_assign_role_to_no_exist_user_from_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/role/all_can_assign", headers=headers)
        roles = response.json()["items"]
        user_role = list(filter(lambda role: "user" == role["name_en"], roles))
        role_key = user_role[0]["key"]

        response = await ac.post(
            f"/role/assign?user_key={NO_EXIST_KEY_USER}&role_key={role_key}",
            headers=headers,
        )
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "User not found"


@pytest.mark.asyncio
async def test_assign_exist_role_to_user_from_super_admin():
    headers = await get_header(SUPER_ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/user/profile/{USER_TEST_USERNAME}",
        )
        user_key = response.json()["key"]

        response = await ac.get("/role/all_can_assign", headers=headers)
        roles = response.json()["items"]
        admin_role = list(filter(lambda role: "admin" == role["name_en"], roles))
        user_role = list(filter(lambda role: "user" == role["name_en"], roles))
        role_key = admin_role[0]["key"]

        response = await ac.post(
            f"/role/assign?user_key={user_key}&role_key={role_key}", headers=headers
        )
    assert response.status_code == 200
    result = response.json()
    assert "name_en" in result
    assert result["name_en"] == "admin"

    role_key = user_role[0]["key"]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/role/assign?user_key={user_key}&role_key={role_key}", headers=headers
        )

    assert response.status_code == 200
    result = response.json()
    assert "name_en" in result
    assert result["name_en"] == "user"


@pytest.mark.asyncio
async def test_assign_role_to_admin_from_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/user/profile/{SUPER_ADMIN_TEST_USERNAME}",
        )
        user_key = response.json()["key"]

        response = await ac.post(
            f"/role/assign?user_key={user_key}&role_key={NO_EXIST_ROLE_KEY}",
            headers=headers,
        )
    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )


@pytest.mark.asyncio
async def test_assign_no_exist_role_to_user_from_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/user/profile/{USER_TEST_USERNAME}",
        )
        user_key = response.json()["key"]

        response = await ac.post(
            f"/role/assign?user_key={user_key}&role_key={NO_EXIST_ROLE_KEY}",
            headers=headers,
        )
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Role not found"