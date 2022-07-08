from typing import Union
from fastapi import APIRouter
from controllers.user_controller import UserController
from fastapi import Security, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from models.response_items import ResponseItems
from models.message_model import MessageModel
from models.user_model import UserModelResponse, UserUpdateDataModel
from consts.name_attribute_access_roles import NAME_ATTR_OWNER
from consts.owner_enum import OwnerEnum
from handlers.access_handler import AccessHandler, RoleAccessModel
from consts.name_roles import SUPER_ADMIN, USER, ADMIN

database_handler: AbstractDatabaseHandler = DatabaseHandler()
user_controller = UserController(database_handler)
security = HTTPBearer()
access_handler = AccessHandler(database_handler)

router = APIRouter(tags=["User"])


@router.get("/all", responses={200: {"model": ResponseItems[UserModelResponse]}})
async def get_all_users(
    credentials: HTTPAuthorizationCredentials = Security(security),
    limit: int = None,
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
        return await user_controller.delete_user_by_key(key)

    return await inside_func(key)


@router.put("/update")
async def update_user_by_key(
    key: str,
    user: UserUpdateDataModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
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
    def inside_func(key):
        return user_controller.delete_user_by_key(key)

    return inside_func(key)
