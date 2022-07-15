import pytest
from httpx import AsyncClient

from main import app

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_all_skills():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/skill/all")
    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
