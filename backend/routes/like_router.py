from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import USER
from controllers.like_controller import LikeController
from controllers.post_controller import PostController
from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from drive.drive_handler import DriveHandler
from handlers.access_handler import AccessHandler
from models.role_access_model import RoleAccessModel

security = HTTPBearer()
database_handler: AbstractDatabaseHandler = DatabaseHandler()
drive_handler = DriveHandler()
access_handler = AccessHandler(database_handler)
post_controller = PostController(database_handler, drive_handler)
like_controller = LikeController(database_handler)
router = APIRouter(tags=["Like"])


@router.put("/")
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


@router.delete("/")
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
