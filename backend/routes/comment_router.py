from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_attribute_access_roles import NAME_ATTR_OWNER
from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from consts.owner_enum import OwnerEnum
from controllers.comment_controller import CommentController
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler
from models.comment_model import CommentInputModel, CommentModel
from models.http_error import HTTPError
from models.role_access_model import RoleAccessModel

security = HTTPBearer()
router = APIRouter(tags=["Comment"])
database_handler = DatabaseHandler()
access_handler = AccessHandler(database_handler)
comment_controller = CommentController(database_handler)


@router.post(
    "/",
    responses={
        200: {"model": CommentModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid or 
            adding a comment to the message failed""",
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
            "description": "If post in not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Adding a comment to a post",
)
async def post_comment(
    post_key: str,
    comment: CommentInputModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(comment, post_key, token):
        return await comment_controller.post_comment(comment, post_key, token)

    return await inside_func(comment, post_key, credentials.credentials)


@router.delete(
    "/",
    responses={
        200: {"model": CommentModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid or
            the comment to the post failed to delete""",
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
            "description": "If post or comment in not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Adding a comment to a post",
)
async def delete_comment(
    comment_key: str,
    post_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
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
        await comment_controller.get_author_key_by_comment_key(comment_key, post_key),
    )
    async def inside_func(comment_key, post_key):
        return await comment_controller.delete_comment(comment_key, post_key)

    return await inside_func(comment_key, post_key)
