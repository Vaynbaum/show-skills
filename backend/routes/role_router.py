from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from consts.name_attribute_access_roles import NAME_ATTR_TO_ASSIGN
from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from controllers.role_controller import RoleController
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler
from models.http_error import HTTPError
from models.response_items import ResponseItems
from models.role_access_model import RoleAccessModel
from models.role_model import RoleInDBModel, RoleModelResponse

security = HTTPBearer()
database_handler = DatabaseHandler()
access_handler = AccessHandler(database_handler)
role_controller = RoleController(database_handler)
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
            "description": "If authentication failed, invalid authentication credentials or no access rights to this method",
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
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=SUPER_ADMIN), RoleAccessModel(name=ADMIN)],
    )
    async def inside_func():
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
            "description": "If authentication failed, invalid authentication credentials or no access rights to this method",
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
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccessModel(
                name=SUPER_ADMIN, attributes={NAME_ATTR_TO_ASSIGN: [ADMIN, USER]}
            ),
            RoleAccessModel(
                name=ADMIN, attributes={NAME_ATTR_TO_ASSIGN: [ADMIN, USER]}
            ),
        ],
        False,
    )
    @access_handler.maker_assign_access(user_key)
    async def inside_func(role_key, user_key):
        return await role_controller.assign_role_to_user(role_key, user_key)

    return await inside_func(role_key, user_key)
