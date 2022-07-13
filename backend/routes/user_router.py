from fastapi import APIRouter, Path, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from consts.name_attribute_access_roles import NAME_ATTR_OWNER
from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from consts.owner_enum import OwnerEnum
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler, RoleAccessModel
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.response_items import ResponseItems
from models.user_model import UserAdditionalDataModel, UserModelResponse

database_handler = DatabaseHandler()
user_controller = UserController(database_handler)
event_controller = EventController(database_handler)
security = HTTPBearer()
access_handler = AccessHandler(database_handler)

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


@router.get(
    "/profile/{username}",
    responses={
        200: {"model": UserModelResponse},
    },
    summary="Getting a user information by username from the database",
)
async def get_user_by_username(username: str = Path(example="ivanov")):
    return await user_controller.get_user_by_username(username)


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


@router.put(
    "/additional_data",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or the user data update was not successful",
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
    async def inside_func(user, key):
        return await user_controller.update_additional_user_data_by_key(user, key)

    return await inside_func(user, key)
