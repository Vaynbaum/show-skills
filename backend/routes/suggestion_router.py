from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from controllers.suggestion_controller import SuggestionController
from db.database_handler import DatabaseHandler
from depends.get_db import get_db
from handlers.access.role_access import RoleAccess
from handlers.access_handler import AccessHandler
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.response_items import ResponseItems
from models.suggestion_model import (
    SuggestionInDBModel,
    SuggestionInputModel,
    SuggestionTickModel,
)

security = HTTPBearer()
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
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(suggestion, token):
        suggestion_controller = SuggestionController(db)
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
    readed: bool = Query(default=False),
    completed: bool = Query(default=False),
    limit: int = Query(default=1000),
    last_key: str = Query(default=None),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(SUPER_ADMIN), RoleAccess(ADMIN)],
    )
    async def inside_func(readed, completed):
        suggestion_controller = SuggestionController(db)
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
    suggestion_key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(SUPER_ADMIN), RoleAccess(ADMIN)],
    )
    async def inside_func(suggestion, suggestion_key):
        suggestion_controller = SuggestionController(db)
        return await suggestion_controller.tick_suggestion(suggestion, suggestion_key)

    return await inside_func(suggestion, suggestion_key)
