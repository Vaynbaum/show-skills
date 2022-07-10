from typing import Union
from fastapi import APIRouter
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from fastapi import Security, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from models.response_items import ResponseItems
from models.message_model import MessageModel
from models.user_model import UserAdditionalDataModel, UserModelResponse
from consts.name_attribute_access_roles import NAME_ATTR_OWNER
from consts.owner_enum import OwnerEnum
from handlers.access_handler import AccessHandler, RoleAccessModel
from consts.name_roles import SUPER_ADMIN, USER, ADMIN

database_handler: AbstractDatabaseHandler = DatabaseHandler()
user_controller = UserController(database_handler)
event_controller = EventController(database_handler)
security = HTTPBearer()
access_handler = AccessHandler(database_handler)

router = APIRouter(tags=["User"])


@router.get("/all", responses={200: {"model": ResponseItems[UserModelResponse]}})
async def get_all_users(
    credentials: HTTPAuthorizationCredentials = Security(security),
    limit: int = 1000,
    last_user_key: str = None,
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=SUPER_ADMIN), RoleAccessModel(name=ADMIN)],
    )
    async def inside_func(limit, last_user_key):
        return await user_controller.get_user_all(limit, last_user_key)

    return await inside_func(limit, last_user_key)


@router.get("/page/{username}", responses={200: {"model": UserModelResponse}})
async def get_user_by_username(username: str = Path(example="ivanov")):
    return await user_controller.get_user_by_username(username)


@router.delete("/", responses={200: {"model": MessageModel}})
async def delete_user_by_key(
    key: str, credentials: HTTPAuthorizationCredentials = Security(security)
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccessModel(
                name=SUPER_ADMIN, attributes={NAME_ATTR_OWNER: OwnerEnum.ANY}
            ),
            RoleAccessModel(name=ADMIN, attributes={NAME_ATTR_OWNER: OwnerEnum.OWN}),
            RoleAccessModel(name=USER, attributes={NAME_ATTR_OWNER: OwnerEnum.OWN}),
        ],
        False,
    )
    @access_handler.maker_owner_access(key)
    async def inside_func(key):
        await event_controller.delete_event_by_user(key)
        return await user_controller.delete_user_by_key(key)

    return await inside_func(key)


@router.put("/additional_data")
async def update_additional_user_data_by_key(
    key: str,
    user: UserAdditionalDataModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccessModel(name=USER),
        ],
    )
    async def inside_func(user,key):
        return await user_controller.update_additional_user_data_by_key(user,key)

    return await inside_func(user,key)
