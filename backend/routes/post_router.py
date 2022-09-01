from fastapi import APIRouter, Depends, Query, UploadFile, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from controllers.post_controller import PostController
from db.database_handler import DatabaseHandler
from depends.get_db import get_db
from depends.get_drive import get_drive
from handlers.access.role_access import RoleAccess
from handlers.drive_handler import DriveHandler
from handlers.access_handler import AccessHandler
from handlers.access.owner.any_owner import AnyOwner
from handlers.access.owner.own_owner import OwnOwner
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.post_model import PostInDBModel, PostInputModel
from models.unload_content_post_model import UnloadContentPostModel
from models.response_items import ResponseItems

security = HTTPBearer()
router = APIRouter(tags=["Post"])


@router.post(
    "/create",
    responses={
        200: {"model": PostInDBModel},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or the post failed to add",
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
    summary="Adding a new post to the database",
)
async def create_post(
    post: PostInputModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(post, token):
        post_controller = PostController(db, drive)
        return await post_controller.create_post(post, token)

    return await inside_func(post, credentials.credentials)


@router.post(
    "/upload/image",
    responses={
        200: {"model": str},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid,
            the image format is invalid or the upload failed""",
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
    summary="Uploading an image to disk",
)
async def upload_image_to_post(
    file: UploadFile,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(file):
        post_controller = PostController(db, drive)
        return post_controller.upload_photo(file)

    return await inside_func(file)


@router.get(
    "/photo/{name_image}",
    responses={
        200: {"description": "File in the format *StreamingResponse*"},
        400: {
            "model": HTTPError,
            "description": "if the file could not be retrieved",
        },
    },
    summary="Getting the photo by the name",
)
async def get_image_by_name(
    name_image: str = Path(example="python.png"),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    post_controller = PostController(db, drive)
    return post_controller.get_photo(name_image)


@router.get(
    "/content/{name_content}",
    responses={
        200: {"description": "File in the format *StreamingResponse*"},
        400: {
            "model": HTTPError,
            "description": "if the file could not be retrieved",
        },
    },
    summary="Getting the content by the name",
)
async def get_content_by_name(
    name_content: str = Path(example="post_uml_zgqeuipptbrjwhd.html"),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    post_controller = PostController(db, drive)
    return post_controller.get_content(name_content)


@router.post(
    "/upload/content",
    responses={
        200: {"model": str},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or the upload failed",
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
    summary="Uploading an post content to disk",
)
async def upload_content_to_post(
    content: UnloadContentPostModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(content_html, name_post):
        post_controller = PostController(db, drive)
        return post_controller.upload_content(content_html, name_post)

    return await inside_func(content.content, content.name)


@router.get(
    "/all",
    responses={200: {"model": ResponseItems[PostInDBModel]}},
    summary="Getting all posts from the database",
)
async def get_all_posts(
    limit: int = Query(default=100),
    last_user_key: str = Query(default=None),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    post_controller = PostController(db, drive)
    return await post_controller.get_all_post(limit, last_user_key)


@router.get(
    "/by_skill",
    responses={200: {"model": ResponseItems[PostInDBModel]}},
    summary="Getting posts by skill name from the database",
)
async def get_posts_by_skill(
    name_skill: str = Query(example="Питон"),
    limit: int = Query(default=100),
    last_user_key: str = Query(default=None),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    post_controller = PostController(db, drive)
    return await post_controller.get_posts_by_skill(name_skill, limit, last_user_key)


@router.delete(
    "/",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid""",
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
            "description": "Post is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Deleting a post by key",
)
async def delete_post_by_key(
    post_key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)
    post_controller = PostController(db, drive)

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
        await post_controller.get_author_key_by_post_key(post_key),
    )
    async def inside_func(post_key):
        return await post_controller.delete_post_by_key(post_key)

    return await inside_func(post_key)


@router.put(
    "/",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid or 
            the post data update was not successful""",
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
            "description": "If the post is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Updating of post data",
)
async def edit_post(
    post: PostInputModel,
    post_key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)
    post_controller = PostController(db, drive)

    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccess(USER, owners=[OwnOwner()]),
        ],
        False,
    )
    @access_handler.maker_owner_access(
        await post_controller.get_author_key_by_post_key(post_key),
    )
    async def inside_func(post, post_key):
        return await post_controller.update_post(post, post_key)

    return await inside_func(post, post_key)
