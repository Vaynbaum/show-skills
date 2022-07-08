from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_attribute_access_roles import NAME_ATTR_OWNER
from consts.owner_enum import OwnerEnum
from controllers.event_controller import EventController
from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler
from models.event_model import EventModelInput
from models.role_access_model import RoleAccessModel
from consts.name_roles import ADMIN, SUPER_ADMIN, USER

security = HTTPBearer()
database_handler: AbstractDatabaseHandler = DatabaseHandler()
access_handler = AccessHandler(database_handler)
event_controller = EventController(database_handler)
router = APIRouter(tags=["Event"])


@router.post("/create")
async def create_event(
    event: EventModelInput,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(event, token):
        return await event_controller.create_event(event, token)

    return await inside_func(event, credentials.credentials)


@router.get("/all")
async def get_all_events(
    credentials: HTTPAuthorizationCredentials = Security(security),
    limit: int = None,
    last_event_key: str = None,
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=ADMIN), RoleAccessModel(name=SUPER_ADMIN)],
    )
    async def inside_func(limit, last_event_key):
        return await event_controller.get_all_events(limit, last_event_key)

    return await inside_func(limit, last_event_key)


@router.get("/subscription")
async def get_events_by_subscription(
    next_days: int = None,
    limit: int = None,
    last_event_key: str = None,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=USER)],
    )
    async def inside_func(next_days, token, limit, last_event_key):
        return await event_controller.get_events_by_subscription(
            next_days, token, limit, last_event_key
        )

    return await inside_func(next_days, credentials.credentials, limit, last_event_key)


@router.get("/user")
async def get_events_by_user(
    key: str,
    limit: int = None,
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


@router.delete("/delete")
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
        await event_controller.get_key_author_by_event_key(key),
    )
    async def inside_func(key):
        return await event_controller.delete_event(key)

    return await inside_func(key)


@router.put("/edit")
async def edit_event(
    event_key: str,
    event: EventModelInput,
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
        await event_controller.get_key_author_by_event_key(event_key),
    )
    async def inside_func(event, event_key):
        return await event_controller.update_event(event, event_key)

    return await inside_func(event, event_key)
