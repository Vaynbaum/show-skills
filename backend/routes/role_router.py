from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security
from consts.name_attribute_access_roles import NAME_ATTR_TO_ASSIGN
from consts.name_roles import ADMIN, SUPER_ADMIN, USER
from controllers.role_controller import RoleController

from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from handlers.access_handler import AccessHandler
from models.role_access_model import RoleAccessModel

security = HTTPBearer()
database_handler: AbstractDatabaseHandler = DatabaseHandler()
access_handler = AccessHandler(database_handler)
role_controller = RoleController(database_handler)
router = APIRouter(tags=["Role"])


@router.get("/all_can_assign")
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


@router.post("/assign")
async def assign_role(
    role_key,
    user_key,
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
