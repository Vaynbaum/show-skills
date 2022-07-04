from typing import Union
from fastapi import APIRouter
from controllers.user_controller import UserController
from fastapi import Security, Path, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from models.items import ResponseItems
from models.message_model import MessageModel
from models.user_model import ResponseUserModel, UserUpdateDataModel
from handlers.role_access.enums.owner_enum import OwnerEnum
from handlers.role_access.role_access_handler import AccessHandler, RoleAccessModel
from consts.datastore import SUPER_ADMIN, USER, ADMIN

database_handler: AbstractDatabaseHandler = DatabaseHandler()
user_controller = UserController(database_handler)
security = HTTPBearer()
role_access_handler = AccessHandler(database_handler)

router = APIRouter(tags=["User"])


@router.get("/all", responses={200: {"model": ResponseItems[ResponseUserModel]}})
async def get_users(
    credentials: HTTPAuthorizationCredentials = Security(security),
    limit: Union[int, None] = None,
    last_user_key: Union[str, None] = None,
):
    @role_access_handler.maker_role_access(
        credentials, [RoleAccessModel(name=SUPER_ADMIN), RoleAccessModel(name=ADMIN)]
    )
    async def inside_func():
        return await user_controller.get_user_all(limit, last_user_key)

    return await inside_func()


@router.get("/{username}", responses={200: {"model": ResponseUserModel}})
async def get_by_username(username: str = Path(example="ivanov")):
    return await user_controller.get_user_by_username(username)


@router.delete("/", responses={200: {"model": MessageModel}})
async def delete_by_key(
    key: str, credentials: HTTPAuthorizationCredentials = Security(security)
):
    @role_access_handler.maker_role_access(
        credentials,
        [
            RoleAccessModel(name=SUPER_ADMIN, owner=OwnerEnum.ANY),
            RoleAccessModel(name=ADMIN, owner=OwnerEnum.OWN),
            RoleAccessModel(name=USER, owner=OwnerEnum.OWN),
        ],
        False,
    )
    @role_access_handler.maker_owner_access(key)
    async def inside_func(key):
        return await user_controller.delete_user_by_key(key)

    return await inside_func(key)


@router.put("/")
async def update_by_key(
    key: str,
    user: UserUpdateDataModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @role_access_handler.maker_role_access(
        credentials,
        [
            RoleAccessModel(name=SUPER_ADMIN, owner=OwnerEnum.ANY),
            RoleAccessModel(name=ADMIN, owner=OwnerEnum.OWN),
            RoleAccessModel(name=USER, owner=OwnerEnum.OWN),
        ],
        False,
    )
    @role_access_handler.maker_owner_access(key)
    def inside_func(key):
        return user_controller.delete_user_by_key(key)

    return inside_func(key)
