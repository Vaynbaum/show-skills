from fastapi import APIRouter, UploadFile, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_attribute_access_roles import NAME_ATTR_OWNER
from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from consts.owner_enum import OwnerEnum
from controllers.post_controller import PostController
from db.database_handler import DatabaseHandler
from handlers.drive_handler import DriveHandler
from handlers.access_handler import AccessHandler
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.post_model import PostInDBModel, PostInputModel
from models.response_items import ResponseItems
from models.role_access_model import RoleAccessModel

security = HTTPBearer()
database_handler = DatabaseHandler()
drive_handler = DriveHandler()
post_controller = PostController(database_handler, drive_handler)
access_handler = AccessHandler(database_handler)
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
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(post, token):
        return await post_controller.create_post(post, token)

    return await inside_func(post, credentials.credentials)


@router.post(
    "/upload_image",
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
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(file):
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
):
    return post_controller.get_photo(name_image)


@router.get(
    "/all",
    responses={200: {"model": ResponseItems[PostInDBModel]}},
    summary="Getting all posts from the database",
)
async def get_all_posts(limit: int = 100, last_user_key: str = None):
    return await post_controller.get_all_post(limit, last_user_key)


@router.get(
    "/by_skill",
    responses={200: {"model": ResponseItems[PostInDBModel]}},
    summary="Getting posts by skill name from the database",
)
async def get_posts_by_skill(
    name_skill: str, limit: int = 100, last_user_key: str = None
):
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
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Updating of post data",
)
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
