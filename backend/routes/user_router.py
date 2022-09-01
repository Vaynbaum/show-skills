from fastapi import APIRouter, Depends, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from db.database_handler import DatabaseHandler
from depends.get_db import get_db
from handlers.access.owner.any_owner import AnyOwner
from handlers.access.owner.own_owner import OwnOwner
from handlers.access.role_access import RoleAccess
from handlers.access_handler import AccessHandler
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.response_items import ResponseItems
from models.user_model import FullUserModelResponse, UserAdditionalDataModel, UserModelResponse

security = HTTPBearer()
router = APIRouter(tags=["User"])


@router.get(
    "/all",
    responses={
        200: {"model": ResponseItems[UserModelResponse]},
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
    summary="Getting all users from the database",
)
async def get_all_users(
    credentials: HTTPAuthorizationCredentials = Security(security),
    limit: int = Query(default=1000),
    last_user_key: str = Query(default=None),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(SUPER_ADMIN), RoleAccess(ADMIN)],
    )
    async def inside_func(limit, last_user_key):
        user_controller = UserController(db)
        return await user_controller.get_user_all(limit, last_user_key)

    return await inside_func(limit, last_user_key)


@router.get(
    "/profile/{username}",
    responses={
        200: {"model": UserModelResponse},
    },
    summary="Getting a user information by username from the database",
)
async def get_user_by_username(
    username: str = Path(example="ivanov"),
    db: DatabaseHandler = Depends(get_db),
):
    user_controller = UserController(db)
    return await user_controller.get_user_by_username(username)


@router.get(
    "/my",
    responses={
        200: {"model": FullUserModelResponse},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, invalid data
            or the user data update was not successful""",
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
    summary="Getting a user information by token from the database",
)
async def get_user_by_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    user_controller = UserController(db)
    user = await user_controller.get_user_by_token(credentials.credentials)
    print(user)
    return FullUserModelResponse(**user.dict())


@router.delete(
    "/",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or events are not deleted",
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
    summary="Deleting a user by key",
)
async def delete_user_by_key(
    key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccess(SUPER_ADMIN, owners=[AnyOwner()]),
            RoleAccess(ADMIN, owners=[OwnOwner()]),
            RoleAccess(USER, owners=[OwnOwner()]),
        ],
        False,
    )
    @access_handler.maker_owner_access(key)
    async def inside_func(key):
        user_controller = UserController(db)
        event_controller = EventController(db)
        await event_controller.delete_event_by_user(key)
        return await user_controller.delete_user_by_key(key)

    return await inside_func(key)


@router.put(
    "/additional_data",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, invalid data
            or the user data update was not successful""",
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
    summary="Changes to additional user data",
)
async def update_additional_user_data_by_key(
    user: UserAdditionalDataModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(user, token):
        user_controller = UserController(db)
        return await user_controller.update_additional_user_data_by_key(user, token)

    return await inside_func(user, credentials.credentials)
