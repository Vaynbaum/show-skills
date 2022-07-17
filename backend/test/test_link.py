import pytest
from httpx import AsyncClient

from main import app
from test.common import *
from test.data.link_data import *
from test.data.user_auth_data import *

pytest_plugins = ("pytest_asyncio",)

# ----------------------Add link----------------------
@pytest.mark.asyncio
async def test_add_delete_new_link():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/link/add", json=LINK_DATA, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Link successfully added"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        url = LINK_DATA["url"]
        response = await ac.delete(f"/link/remove?url_link={url}", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 0


@pytest.mark.asyncio
async def test_add_link_alredy_exist():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/link/add", json=LINK_DATA, headers=headers)
        response = await ac.post("/link/add", json=LINK_DATA, headers=headers)
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Link already exists"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        url = LINK_DATA["url"]
        await ac.delete(f"/link/remove?url_link={url}", headers=headers)


# ----------------------Remove link----------------------
@pytest.mark.asyncio
async def test_delete_no_exist_link():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        url = LINK_DATA["url"]
        response = await ac.delete(f"/link/remove?url_link={url}", headers=headers)
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Link not found"
