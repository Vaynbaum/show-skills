import pytest
from httpx import AsyncClient

from main import app
from test.data.auth_data import *
from test.data.user_auth_data import *
from test.common import *


pytest_plugins = ("pytest_asyncio",)

# ----------------------Registration----------------------
@pytest.mark.asyncio
async def test_registration_invalid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/signup",
            json={
                "email": IVANOV_EMAIL,
                "username": IVANOV_USERNAME,
                "password": PASSWORD,
                "firstname": IVANOV_LASTNAME,
            },
        )
    assert response.status_code == 422
    result = response.json()
    assert "detail" in result
    assert result["detail"][0] is not None


@pytest.mark.asyncio
async def test_registration_valid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/signup",
            json=IVANOV_REGISTRATION_VALID_DATA,
        )
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Registration is successful"

    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_again_registration_valid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        response = await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
    assert response.status_code == 401
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Account already exists"

    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_registration_username_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        response = await ac.post("/auth/signup", json=IVANOV1_REGISTRATION_INVALID_DATA)
    assert response.status_code == 401
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Username is already used"

    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


# ----------------------Auth----------------------
@pytest.mark.asyncio
async def test_auth_valid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        response = await ac.post("/auth/login", json=IVANOV_AUTH_VALID_DATA)
    assert response.status_code == 200
    result = response.json()
    assert "access_token" in result
    assert "refresh_token" in result
    assert result["access_token"] is not None
    assert result["refresh_token"] is not None

    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_auth_no_exist_account():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json=PETROV_AUTH_VALID_DATA)
    assert response.status_code == 401
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Invalid email"


@pytest.mark.asyncio
async def test_auth_invalid_password():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        response = await ac.post("/auth/login", json=IVANOV_AUTH_INVALID_DATA)
    assert response.status_code == 401
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Invalid password"

    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


# ----------------------Refresh token----------------------
@pytest.mark.asyncio
async def test_refresh_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json=USER_TEST_AUTH)
        token = response.json()["refresh_token"]
        response = await ac.get(
            "/auth/refresh_token", headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    result = response.json()
    assert "access_token" in result
    assert result["access_token"] is not None
