import pytest
from httpx import AsyncClient

from main import app
from test.common import *
from test.data.event_data import *
from test.data.user_auth_data import *

pytest_plugins = ("pytest_asyncio",)

# ----------------------Create event----------------------
@pytest.mark.asyncio
async def test_create_delete_event_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/event/create", json=EVENT_VALID_DATA, headers=headers
        )
    assert response.status_code == 200
    result = response.json()
    event_key = result["key"]
    assert event_key is not None
    assert result["author"]["username"] == USER_TEST_USERNAME

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/event/delete?key={event_key}", headers=headers)

    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Deletion successful"


@pytest.mark.asyncio
async def test_create_already_exist_event_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/event/create", json=EVENT_VALID_DATA, headers=headers
        )
        event_key = response.json()["key"]
        response = await ac.post(
            "/event/create", json=EVENT_VALID_DATA, headers=headers
        )

    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Event already exists"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/event/delete?key={event_key}", headers=headers)


@pytest.mark.asyncio
async def test_create_event_invalid_data_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/event/create", json=EVENT_INVALID_DATA, headers=headers
        )

    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Invalid year"


# ----------------------All events----------------------
@pytest.mark.asyncio
async def test_get_all_events():
    admin_headers = await get_header(ADMIN_TEST_AUTH)
    user_headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/event/all", headers=admin_headers)

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/event/create", json=EVENT_VALID_DATA, headers=user_headers
        )
    event_key = response.json()["key"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/event/all?limit=1", headers=admin_headers)

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert result["count"] == 1

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/event/delete?key={event_key}", headers=user_headers
        )


# ----------------------Get user's events by subscriptions----------------------
@pytest.mark.asyncio
async def test_get_my_events_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/event/subscription", headers=headers)

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result


@pytest.mark.asyncio
async def test_get_my_events_user_count_1():
    headers_test_user = await get_header(USER_TEST_AUTH)
    username = IVANOV_REGISTRATION_VALID_DATA["username"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        event_key = await create_event(EVENT_VALID_DATA, IVANOV_AUTH_VALID_DATA)
        await arrange_subscription(username, USER_TEST_AUTH)

        response = await ac.get("/event/subscription", headers=headers_test_user)

    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "count" in result
    assert "last" in result
    assert result["count"] == 1

    await annul_subscription(username, USER_TEST_AUTH)
    await delete_event(event_key, IVANOV_AUTH_VALID_DATA)
    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_get_my_events_user_next_days():
    headers_test_user = await get_header(USER_TEST_AUTH)
    username = IVANOV_REGISTRATION_VALID_DATA["username"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        event_key = await create_event(EVENT_VALID_DATA, IVANOV_AUTH_VALID_DATA)
        await arrange_subscription(username, USER_TEST_AUTH)

        response = await ac.get(
            f"/event/subscription?next_days={1}", headers=headers_test_user
        )

    assert response.status_code == 200
    assert response.json()["count"] == 0

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/event/subscription?next_days={2}", headers=headers_test_user
        )
    assert response.status_code == 200
    assert response.json()["count"] == 1

    await annul_subscription(username, USER_TEST_AUTH)
    await delete_event(event_key, IVANOV_AUTH_VALID_DATA)
    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


# ----------------------Get events by user----------------------
@pytest.mark.asyncio
async def test_get_events_by_user():
    headers_test_user = await get_header(USER_TEST_AUTH)
    headers_test_admin = await get_header(ADMIN_TEST_AUTH)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/user/profile/{USER_TEST_USERNAME}",
        )
        user_key = response.json()["key"]

        response = await ac.get(
            f"/event/user?key={user_key}", headers=headers_test_admin
        )
    assert response.status_code == 200
    assert response.json()["count"] == 0

    event_key = await create_event(EVENT_VALID_DATA, USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/event/user?key={user_key}", headers=headers_test_user
        )
    assert response.status_code == 200
    assert response.json()["count"] == 1

    await delete_event(event_key, USER_TEST_AUTH)


# ----------------------Delete event----------------------
@pytest.mark.asyncio
async def test_delete_event_by_no_exist_key():
    headers_test_admin = await get_header(ADMIN_TEST_AUTH)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/event/delete?key={NO_EXIST_EVENT_KEY}", headers=headers_test_admin
        )
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


@pytest.mark.asyncio
async def test_delete_event_by_key_admin():
    headers_test_admin = await get_header(ADMIN_TEST_AUTH)
    event_key = await create_event(EVENT_VALID_DATA, USER_TEST_AUTH)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/event/delete?key={event_key}", headers=headers_test_admin
        )

    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Deletion successful"


@pytest.mark.asyncio
async def test_delete_event_by_key_other_user():
    headers = await get_header(USER_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=IVANOV_REGISTRATION_VALID_DATA)
        event_key = await create_event(EVENT_VALID_DATA, IVANOV_AUTH_VALID_DATA)
        response = await ac.delete(f"/event/delete?key={event_key}", headers=headers)

    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "There is no access to this method"

    await delete_event(event_key, IVANOV_AUTH_VALID_DATA)
    await delete_auth(IVANOV_REGISTRATION_VALID_DATA)


# ----------------------Edit event----------------------
@pytest.mark.asyncio
async def test_edit_no_exist_event_admin():
    headers_test_admin = await get_header(SUPER_ADMIN_TEST_AUTH)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            f"/event/edit?event_key={NO_EXIST_EVENT_KEY}",
            json=EVENT_VALID_DATA,
            headers=headers_test_admin,
        )

    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Event not found"


@pytest.mark.asyncio
async def test_edit_event_admin():
    headers_test_admin = await get_header(ADMIN_TEST_AUTH)
    event_key = await create_event(EVENT_EDIT_VALID_DATA, USER_TEST_AUTH)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            f"/event/edit?event_key={event_key}",
            json=EVENT_INVALID_DATA,
            headers=headers_test_admin,
        )

    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert (
        result["detail"] == "The user's role is not in the list of roles allowed method"
    )

    await delete_event(event_key, USER_TEST_AUTH)


@pytest.mark.asyncio
async def test_edit_event_other_user():
    headers_test_user = await get_header(USER_TEST_AUTH)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SOBOLEV_REGISTRATION_VALID_DATA)
        event_key = await create_event(EVENT_VALID_DATA, SOBOLEV_AUTH_VALID_DATA)
        response = await ac.put(
            f"/event/edit?event_key={event_key}",
            json=EVENT_INVALID_DATA,
            headers=headers_test_user,
        )

    assert response.status_code == 403
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "There is no access to this method"

    await delete_event(event_key, SOBOLEV_AUTH_VALID_DATA)
    await delete_auth(SOBOLEV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_edit_event_user_invalid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=SMIRNOV_REGISTRATION_VALID_DATA)
        event_key = await create_event(
            EVENT_VALID_DATA, SMIRNOV_REGISTRATION_VALID_DATA
        )
        headers = await get_header(SMIRNOV_AUTH_VALID_DATA)

        response = await ac.put(
            f"/event/edit?event_key={event_key}",
            json=EVENT_INVALID_DATA,
            headers=headers,
        )

    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Invalid year"

    await delete_event(event_key, SMIRNOV_AUTH_VALID_DATA)
    await delete_auth(SMIRNOV_REGISTRATION_VALID_DATA)


@pytest.mark.asyncio
async def test_edit_event_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/signup", json=PETROV_REGISTRATION_VALID_DATA)
        event_key = await create_event(EVENT_VALID_DATA, PETROV_REGISTRATION_VALID_DATA)
        headers = await get_header(PETROV_AUTH_VALID_DATA)
        response = await ac.put(
            f"/event/edit?event_key={event_key}",
            json=EVENT_EDIT_VALID_DATA,
            headers=headers,
        )

    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert result["message"] == "Editing successful"

    await delete_event(event_key, PETROV_AUTH_VALID_DATA)
    await delete_auth(PETROV_REGISTRATION_VALID_DATA)
