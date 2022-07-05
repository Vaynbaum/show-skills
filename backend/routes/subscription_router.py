from fastapi import APIRouter, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from controllers.subscription_controller import SubscriptionController
from consts.name_roles import USER
from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from handlers.role_access_handler import AccessHandler
from models.role_access_model import RoleAccessModel

database_handler: AbstractDatabaseHandler = DatabaseHandler()
role_access_handler = AccessHandler(database_handler)
subscription_controller = SubscriptionController(database_handler)
security = HTTPBearer()

router = APIRouter(tags=["Subscription"])


@router.post("/arrange")
async def subscribe(
    username_favorite: str = Query(example="ivanov"),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @role_access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(username_favorite, credentials):
        return await subscription_controller.subscribe(
            username_favorite, credentials.credentials
        )

    return await inside_func(username_favorite, credentials)


@router.delete("/annul")
async def annul(
    username_favorite: str = Query(example="ivanov"),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @role_access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(username_favorite, credentials):
        return await subscription_controller.annul(
            username_favorite, credentials.credentials
        )

    return await inside_func(username_favorite, credentials)
