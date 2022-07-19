from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from controllers.comment_controller import CommentController
from db.database_handler import DatabaseHandler
from depends.get_db import get_db
from handlers.access.owner.any_owner import AnyOwner
from handlers.access.owner.own_owner import OwnOwner
from handlers.access.role_access import RoleAccess
from handlers.access_handler import AccessHandler
from models.comment_model import CommentInputModel, CommentModel
from models.http_error import HTTPError

security = HTTPBearer()
router = APIRouter(tags=["Comment"])


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
    comment: CommentInputModel,
    post_key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(comment, post_key, token):
        comment_controller = CommentController(db)
        return await comment_controller.post_comment(comment, post_key, token)

    return await inside_func(comment, post_key, credentials.credentials)


@router.delete(
    "/",
    responses={
        200: {"model": List[CommentModel]},
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
    summary="Deleting a comment to a postt",
)
async def delete_comment(
    comment_key: str = Query(),
    post_key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)
    comment_controller = CommentController(db)

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
        await comment_controller.get_author_key_by_comment_key(comment_key, post_key),
    )
    async def inside_func(comment_key, post_key):
        return await comment_controller.delete_comment(comment_key, post_key)

    return await inside_func(comment_key, post_key)
