import pytest
from httpx import AsyncClient

from main import app
from test.common import *
from test.data.subsribe_data import *
from test.data.user_auth_data import *

pytest_plugins = ("pytest_asyncio",)

# ----------------------Subscribe and annul----------------------
@pytest.mark.asyncio
async def test_subscribe_annul_exist_username():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        username = IVANOV_REGISTRATION_VALID_DATA["username"]
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )

    assert response.status_code == 200
    result = response.json()
    assert "favorite" in result
    assert "follower" in result
    assert result["follower"] is not None
    assert result["favorite"] is not None
    assert result["favorite"]["email"] == IVANOV_REGISTRATION_VALID_DATA["email"]
    assert result["follower"]["email"] == USER_TEST_AUTH["email"]
    result = list(
        filter(
            lambda item: result["follower"]["username"] == item["username"],
            result["favorite"]["followers"],
        )
    )
    assert len(result) > 0

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/subscription/annul?username_favorite={username}", headers=headers
        )
    assert response.status_code == 200
    result = response.json()
    assert "favorite" in result
    assert "follower" in result
    assert result["follower"] is not None
    assert result["favorite"] is not None
    assert result["favorite"]["email"] == IVANOV_REGISTRATION_VALID_DATA["email"]
    assert result["follower"]["email"] == USER_TEST_AUTH["email"]
    result = list(
        filter(
            lambda item: result["follower"]["username"] == item["username"],
            result["favorite"]["followers"],
        )
    )
    assert len(result) == 0

    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_subscribe_annul_no_exist_username():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        username = IVANOV_REGISTRATION_VALID_DATA["username"]
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )

    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Favorite not found"


@pytest.mark.asyncio
async def test_subscribe_no_exist_username():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        username = IVANOV_REGISTRATION_VALID_DATA["username"]
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )

    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Favorite not found"


@pytest.mark.asyncio
async def test_subscribe_to_me():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        username = USER_TEST_USERNAME
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )

    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "You can't subscribe to yourself"


@pytest.mark.asyncio
async def test_subscribe_to_non_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        username = ADMIN_TEST_USERNAME
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )

    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Some of you are non-users"


@pytest.mark.asyncio
async def test_subscribe_from_non_user():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        username = USER_TEST_AUTH
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )

    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )


@pytest.mark.asyncio
async def test_subscribe_already_exist_subscribed():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        username = IVANOV_REGISTRATION_VALID_DATA["username"]
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )

    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Subscription already exists"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/subscription/annul?username_favorite={username}", headers=headers
        )
    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


# ----------------------Annul----------------------
@pytest.mark.asyncio
async def test_annul_subscribe_no_exist_username():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        username = IVANOV_REGISTRATION_VALID_DATA["username"]
        response = await ac.delete(
            f"/subscription/annul?username_favorite={username}", headers=headers
        )

    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Favorite not found"


@pytest.mark.asyncio
async def test_annul_subscribe_no_exist_subscribe():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        username = IVANOV_REGISTRATION_VALID_DATA["username"]
        response = await ac.delete(
            f"/subscription/annul?username_favorite={username}", headers=headers
        )

    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Favorite not found"
    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


# ----------------------All Subscribe----------------------
@pytest.mark.asyncio
async def test_get_my_all_subscribes_admin():
    headers = await get_header(ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/subscription/my", headers=headers)

    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )


@pytest.mark.asyncio
async def test_get_my_all_subscribes_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/subscription/my", headers=headers)

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 0

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        username = IVANOV_REGISTRATION_VALID_DATA["username"]
        response = await ac.post(
            f"/subscription/arrange?username_favorite={username}", headers=headers
        )
        response = await ac.get("/subscription/my", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    favorite = result[0]["favorite"]
    assert favorite["username"] == username

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/subscription/annul?username_favorite={username}", headers=headers
        )
    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)
