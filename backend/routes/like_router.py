from typing import List
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import USER
from controllers.like_controller import LikeController
from controllers.post_controller import PostController
from db.database_handler import DatabaseHandler
from handlers.drive_handler import DriveHandler
from handlers.access_handler import AccessHandler
from models.http_error import HTTPError
from models.like_model import LikeModel
from models.message_model import MessageModel
from models.role_access_model import RoleAccessModel

security = HTTPBearer()
database_handler = DatabaseHandler()
drive_handler = DriveHandler()
access_handler = AccessHandler(database_handler)
post_controller = PostController(database_handler, drive_handler)
like_controller = LikeController(database_handler)
router = APIRouter(tags=["Like"])


@router.put(
    "/",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, 
            the like has already been set or it failed to put a like""",
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
            "description": "If post is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Like the post",
)
async def put_like(
    post_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(post_key, token):
        return await like_controller.put_like(post_key, token)

    return await inside_func(post_key, credentials.credentials)


@router.delete("/",
    responses={
        200: {"model": List[LikeModel]},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid or 
            it is not successful to remove the like""",
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
            "description": "If post or like is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Like the post",)
async def remove_like(
    post_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(post_key, token):
        return await like_controller.remove_like(post_key, token)

    return await inside_func(post_key, credentials.credentials)
