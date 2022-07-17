from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_roles import ADMIN, SUPER_ADMIN
from depends.get_db import get_db
from controllers.role_controller import RoleController
from db.database_handler import DatabaseHandler
from handlers.access.role_access import RoleAccess
from handlers.access_handler import AccessHandler
from handlers.access.assign.admin_assign import AdminAssign
from handlers.access.assign.user_assign import UserAssign
from models.http_error import HTTPError
from models.response_items import ResponseItems
from models.role_model import RoleInDBModel, RoleModelResponse

security = HTTPBearer()
router = APIRouter(tags=["Role"])


@router.get(
    "/all_can_assign",
    responses={
        200: {"model": ResponseItems[RoleInDBModel]},
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
            "description": """If authentication failed, invalid authentication credentials or
            no access rights to this method""",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Getting all roles from the database",
)
async def get_all_rolles_that_can_assign(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(SUPER_ADMIN), RoleAccess(ADMIN)],
    )
    async def inside_func():
        role_controller = RoleController(db)
        return await role_controller.get_all_roles()

    return await inside_func()


@router.post(
    "/assign",
    responses={
        200: {"model": RoleModelResponse},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or the user data update was not successful",
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
            "description": "If the user is not found or the role is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Assign a role to a user",
)
async def assign_role(
    role_key: str,
    user_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccess(SUPER_ADMIN, assigns=[AdminAssign(), UserAssign()]),
            RoleAccess(ADMIN, assigns=[AdminAssign(), UserAssign()]),
        ],
        False,
    )
    @access_handler.maker_assign_access(user_key)
    async def inside_func(role_key, user_key):
        role_controller = RoleController(db)
        return await role_controller.assign_role_to_user(role_key, user_key)

    return await inside_func(role_key, user_key)
