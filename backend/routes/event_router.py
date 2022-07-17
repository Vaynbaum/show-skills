from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from controllers.event_controller import EventController
from db.database_handler import DatabaseHandler
from depends.get_db import get_db
from handlers.access.owner.any_owner import AnyOwner
from handlers.access.owner.own_owner import OwnOwner
from handlers.access.role_access import RoleAccess
from handlers.access_handler import AccessHandler
from models.event_model import EventInDBModel, EventInputModel
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.response_items import ResponseItems
from consts.name_roles import ADMIN, SUPER_ADMIN, USER

security = HTTPBearer()
router = APIRouter(tags=["Event"])


@router.post(
    "/create",
    responses={
        200: {"model": EventInDBModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, the event already exists,
            the event failed to add or year is invalid""",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Adding a new event to the database",
)
async def create_event(
    event: EventInputModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(event, token):
        event_controller = EventController(db)
        return await event_controller.create_event(event, token)

    return await inside_func(event, credentials.credentials)


@router.get(
    "/all",
    responses={
        200: {"model": ResponseItems[EventInDBModel]},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Getting all events from the database",
)
async def get_all_events(
    credentials: HTTPAuthorizationCredentials = Security(security),
    limit: int = 1000,
    last_event_key: str = None,
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(ADMIN), RoleAccess(SUPER_ADMIN)],
    )
    async def inside_func(limit, last_event_key):
        event_controller = EventController(db)
        return await event_controller.get_all_events(limit, last_event_key)

    return await inside_func(limit, last_event_key)


@router.get(
    "/subscription",
    responses={
        200: {"model": ResponseItems[EventInDBModel]},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Getting events by subscriptions",
)
async def get_events_by_subscription(
    next_days: int = None,
    limit: int = 1000,
    last_event_key: str = None,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(USER)],
    )
    async def inside_func(
        token,
        next_days,
        limit,
        last_event_key,
    ):
        event_controller = EventController(db)
        return await event_controller.get_events_by_subscription(
            token,
            next_days,
            limit,
            last_event_key,
        )

    return await inside_func(credentials.credentials, next_days, limit, last_event_key)


@router.get(
    "/user",
    responses={
        200: {"model": ResponseItems[EventInDBModel]},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Getting user events",
)
async def get_events_by_user(
    key: str,
    limit: int = 1000,
    last_event_key: str = None,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccess(SUPER_ADMIN),
            RoleAccess(ADMIN),
            RoleAccess(USER),
        ],
    )
    async def inside_func(key, limit, last_event_key):
        event_controller = EventController(db)
        return await event_controller.get_event_by_user_key(key, limit, last_event_key)

    return await inside_func(key, limit, last_event_key)


@router.delete(
    "/delete",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        404: {
            "model": HTTPError,
            "description": "If the event is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Delete a event from the database by key",
)
async def delete_event(
    key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)
    event_controller = EventController(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccess(SUPER_ADMIN, owners=[AnyOwner()]),
            RoleAccess(ADMIN, owners=[AnyOwner()]),
            RoleAccess(USER, owners=[OwnOwner()]),
        ],
        False,
    )
    @access_handler.maker_owner_access(
        await event_controller.get_author_key_by_event_key(key),
    )
    async def inside_func(key):
        return await event_controller.delete_event(key)

    return await inside_func(key)


@router.put(
    "/edit",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, the event data failed to update
            or year is invalid""",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        404: {
            "model": HTTPError,
            "description": "If the event is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Updating of event data",
)
async def edit_event(
    event_key: str,
    event: EventInputModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)
    event_controller = EventController(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccess(USER, owners=[OwnOwner()]),
        ],
        False,
    )
    @access_handler.maker_owner_access(
        await event_controller.get_author_key_by_event_key(event_key),
    )
    async def inside_func(event, event_key):
        return await event_controller.update_event(event, event_key)

    return await inside_func(event, event_key)
