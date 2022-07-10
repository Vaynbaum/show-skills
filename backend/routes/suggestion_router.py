from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from controllers.suggestion_controller import SuggestionController
from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler
from models.role_access_model import RoleAccessModel
from models.suggestion_model import SuggestionInputModel, SuggestionTickModel

security = HTTPBearer()
database_handler: AbstractDatabaseHandler = DatabaseHandler()
suggestion_controller = SuggestionController(database_handler)
access_handler = AccessHandler(database_handler)
router = APIRouter(tags=["Suggestion"])


@router.post("/")
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


@router.get("/")
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


@router.put("/tick")
async def tick_suggestion(
    suggestion: SuggestionTickModel,
    suggestion_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=SUPER_ADMIN), RoleAccessModel(name=ADMIN)],
    )
    async def inside_func(suggestion,suggestion_key):
        return await suggestion_controller.tick_suggestion(suggestion,suggestion_key)

    return await inside_func(suggestion,suggestion_key)
