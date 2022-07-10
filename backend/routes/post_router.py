from typing import Union
from fastapi import APIRouter, Query, UploadFile, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security
from consts.name_attribute_access_roles import NAME_ATTR_OWNER

from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from consts.owner_enum import OwnerEnum
from controllers.post_controller import PostController
from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from drive.drive_handler import DriveHandler
from handlers.access_handler import AccessHandler
from models.post_model import PostInputModel
from models.role_access_model import RoleAccessModel

security = HTTPBearer()
database_handler: AbstractDatabaseHandler = DatabaseHandler()
drive_handler = DriveHandler()
post_controller = PostController(database_handler, drive_handler)
access_handler = AccessHandler(database_handler)
router = APIRouter(tags=["Post"])


@router.post("/create")
async def create_post(
    post: PostInputModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(post, token):
        return await post_controller.create_post(post, token)

    return await inside_func(post, credentials.credentials)


@router.post("/upload_image")
async def upload_image_to_post(
    file: UploadFile,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(file):
        return post_controller.upload_photo(file)

    return await inside_func(file)


@router.get("/photo/{name_image}")
async def upload_image_to_post(
    name_image: str = Path(example="python.png"),
):
    return post_controller.get_photo(name_image)


@router.get("/all")
async def get_all_posts(limit: int = 100, last_user_key: str = None):
    return await post_controller.get_all_post(limit, last_user_key)


@router.get("/by_skill")
async def get_posts_by_skill(
    name_skill: str, limit: int = 100, last_user_key: str = None
):
    return await post_controller.get_posts_by_skill(name_skill, limit, last_user_key)


@router.delete("/")
async def delete_post_by_key(
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
        await post_controller.get_author_key_by_post_key(post_key),
    )
    async def inside_func(post_key):
        return await post_controller.delete_post_by_key(post_key)

    return await inside_func(post_key)


@router.put("/")
async def edit_post(
    post: PostInputModel,
    post_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(post, post_key):
        return await post_controller.update_post(post, post_key)

    return await inside_func(post, post_key)
