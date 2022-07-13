from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from controllers.suggestion_controller import SuggestionController
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.response_items import ResponseItems
from models.role_access_model import RoleAccessModel
from models.suggestion_model import (
    SuggestionInDBModel,
    SuggestionInputModel,
    SuggestionTickModel,
)

security = HTTPBearer()
database_handler = DatabaseHandler()
suggestion_controller = SuggestionController(database_handler)
access_handler = AccessHandler(database_handler)
router = APIRouter(tags=["Suggestion"])


@router.post(
    "/",
    responses={
        200: {"model": SuggestionInDBModel},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or the suggestion is not sent",
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
    summary="Creating a proposal for the system administration",
)
async def post_suggestion(
    suggestion: SuggestionInputModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(suggestion, token):
        return await suggestion_controller.add_suggestion(suggestion, token)

    return await inside_func(suggestion, credentials.credentials)


@router.get(
    "/",
    responses={
        200: {"model": ResponseItems[SuggestionInDBModel]},
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
    summary="Getting all suggestions from the database",
)
async def get_all_suggestions(
    readed: bool = False,
    completed: bool = False,
    limit: int = 1000,
    last_key: str = None,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=SUPER_ADMIN), RoleAccessModel(name=ADMIN)],
    )
    async def inside_func(readed, completed):
        return await suggestion_controller.get_all_suggestions(
            readed, completed, limit, last_key
        )

    return await inside_func(readed, completed)


@router.put(
    "/tick",
    responses={
        200: {"model": MessageModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid or the suggestion data 
            update was not successful""",
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
    summary="Mark the status of the suggestion",
)
async def tick_suggestion(
    suggestion: SuggestionTickModel,
    suggestion_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=SUPER_ADMIN), RoleAccessModel(name=ADMIN)],
    )
    async def inside_func(suggestion, suggestion_key):
        return await suggestion_controller.tick_suggestion(suggestion, suggestion_key)

    return await inside_func(suggestion, suggestion_key)
