from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from controllers.subscription_controller import SubscriptionController
from consts.name_roles import USER
from db.database_handler import DatabaseHandler
from depends.get_db import get_db
from handlers.access.role_access import RoleAccess
from handlers.access_handler import AccessHandler
from models.http_error import HTTPError
from models.result_subscribe_model import ResultSubscriptionModel
from models.subscription_model import SubscriptionModel


security = HTTPBearer()
router = APIRouter(tags=["Subscription"])


@router.post(
    "/arrange",
    responses={
        200: {"model": ResultSubscriptionModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, there is an attempt to subscribe to yourself, 
            not a user, a subscription already exists or it failed to subscribe""",
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
            "description": "If the favorite is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Subscribing to another user",
)
async def subscribe(
    username_favorite: str = Query(example="ivanov"),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(username_favorite, credentials):
        subscription_controller = SubscriptionController(db)
        return await subscription_controller.subscribe(
            username_favorite, credentials.credentials
        )

    return await inside_func(username_favorite, credentials)


@router.delete(
    "/annul",
    responses={
        200: {"model": ResultSubscriptionModel},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or unsubscribe failed",
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
            "description": "If the favorite is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Cancel subscription",
)
async def annul(
    username_favorite: str = Query(example="ivanov"),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(username_favorite, credentials):
        subscription_controller = SubscriptionController(db)
        return await subscription_controller.annul(
            username_favorite, credentials.credentials
        )

    return await inside_func(username_favorite, credentials)


@router.get(
    "/my",
    responses={
        200: {"model": List[SubscriptionModel]},
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
    summary="Getting all of my subscriptions",
)
async def get_my_subscription(
    limit: int = None,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(credentials.credentials, [RoleAccess(USER)])
    async def inside_func(token, limit):
        subscription_controller = SubscriptionController(db)
        return await subscription_controller.get_subscriptions(token, limit)

    return await inside_func(credentials.credentials, limit)
