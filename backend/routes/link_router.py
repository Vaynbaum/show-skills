from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import USER
from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from handlers.role_access_handler import AccessHandler
from models.role_access_model import RoleAccessModel
from models.link_model import LinkModel
from controllers.link_controller import LinkController

security = HTTPBearer()
database_handler: AbstractDatabaseHandler = DatabaseHandler()
role_access_handler = AccessHandler(database_handler)
link_controller = LinkController(database_handler)

router = APIRouter(tags=["Link"])


@router.post("/add")
async def add_link(
    link: LinkModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @role_access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(link, token):
        return await link_controller.add_link(link, token)

    return await inside_func(link, credentials.credentials)


@router.delete("/remove")
async def remove_link(
    url_link: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @role_access_handler.maker_role_access(
        credentials.credentials, [RoleAccessModel(name=USER)]
    )
    async def inside_func(url_link, token):
        return await link_controller.remove_link(url_link, token)

    return await inside_func(url_link, credentials.credentials)
