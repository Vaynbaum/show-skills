from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_attribute_access_roles import NAME_ATTR_OWNER
from consts.owner_enum import OwnerEnum
from controllers.event_controller import EventController
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler
from models.event_model import EventInDBModel, EventInputModel
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.response_items import ResponseItems
from models.role_access_model import RoleAccessModel
from consts.name_roles import ADMIN, SUPER_ADMIN, USER

security = HTTPBearer()
database_handler = DatabaseHandler()
access_handler = AccessHandler(database_handler)
event_controller = EventController(database_handler)
router = APIRouter(tags=["Event"])


@router.post(
    "/create",
    responses={
        200: {"model": EventInDBModel},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or the event already exists",
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
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(event, token):
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
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=ADMIN), RoleAccessModel(name=SUPER_ADMIN)],
    )
    async def inside_func(limit, last_event_key):
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
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=USER)],
    )
    async def inside_func(token, limit, last_event_key, next_days):
        return await event_controller.get_events_by_subscription(
            token, limit, last_event_key, next_days
        )

    return await inside_func(credentials.credentials, limit, last_event_key, next_days)


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
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccessModel(name=SUPER_ADMIN),
            RoleAccessModel(name=ADMIN),
            RoleAccessModel(name=USER),
        ],
    )
    async def inside_func(key, limit, last_event_key):
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
    key: str, credentials: HTTPAuthorizationCredentials = Security(security)
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccessModel(
                name=SUPER_ADMIN, attributes={NAME_ATTR_OWNER: OwnerEnum.ANY}
            ),
            RoleAccessModel(name=ADMIN, attributes={NAME_ATTR_OWNER: OwnerEnum.ANY}),
            RoleAccessModel(name=USER, attributes={NAME_ATTR_OWNER: OwnerEnum.OWN}),
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
            "description": "If the user key is invalid or the event data failed to update",
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
async def edit_event(
    event_key: str,
    event: EventInputModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccessModel(name=USER, attributes={NAME_ATTR_OWNER: OwnerEnum.OWN}),
        ],
        False,
    )
    @access_handler.maker_owner_access(
        await event_controller.get_author_key_by_event_key(event_key),
    )
    async def inside_func(event, event_key):
        return await event_controller.update_event(event, event_key)

    return await inside_func(event, event_key)
