from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import USER
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.role_access_model import RoleAccessModel
from models.link_model import LinkModel
from controllers.link_controller import LinkController

security = HTTPBearer()
database_handler = DatabaseHandler()
access_handler = AccessHandler(database_handler)
link_controller = LinkController(database_handler)

router = APIRouter(tags=["Link"])


@router.post(
    "/add",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, 
            the link already exists or the link failed to add """,
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
    summary="Add a link to your account in another social network",
)
async def add_link(
    link: LinkModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(link, token):
        return await link_controller.add_link(link, token)

    return await inside_func(link, credentials.credentials)


@router.delete(
    "/remove",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid or the link failed to delete""",
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
            "description": "If the link is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Delete a link to your account on another social network",
)
async def remove_link(
    url_link: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(url_link, token):
        return await link_controller.remove_link(url_link, token)

    return await inside_func(url_link, credentials.credentials)
