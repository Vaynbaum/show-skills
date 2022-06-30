from fastapi import APIRouter
from controllers.user_controller import UserController
from fastapi import Security, Path, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from db.models.user_model import UserResponseModel
from handlers.role_access_handler import AccessHandler, OwnerEnum, RoleModel
from set_role_system.datastore import SUPER_ADMIN, USER, ADMIN

database_handler: AbstractDatabaseHandler = DatabaseHandler()
auth_controller = UserController(database_handler)
user_controller = UserController(database_handler)
security = HTTPBearer()
role_access_handler = AccessHandler(database_handler)

router = APIRouter(tags=['User'])


@router.get("/all")
def get_users(
        credentials: HTTPAuthorizationCredentials = Security(security),
        limit: int | None = 100, 
        last_user_key: str | None = None
    ):
    @role_access_handler.maker_role_access(credentials=credentials, roles=[
        {"name": SUPER_ADMIN},
        {"name": ADMIN}
    ])
    def inside_func():
        return user_controller.get_user_all(limit, last_user_key)
        # return user_controller.delete_user_by_key(key)
    return inside_func()


@router.get("/{username}")
def get_by_username(username: str | None = Path(example="ivanov")):
    return auth_controller.get_user_by_username(username)


@router.delete("/delete")
def delete_by_key(key: str, credentials: HTTPAuthorizationCredentials = Security(security)):
    @role_access_handler.maker_role_access(credentials=credentials, roles=[
        {"name": SUPER_ADMIN, "owner": OwnerEnum.ANY},
        {"name": ADMIN, "owner": OwnerEnum.OWN},
        {"name": USER, "owner": OwnerEnum.OWN}
    ], key_author=key)
    def inside_func(key):
        return user_controller.delete_user_by_key(key)
    return inside_func(key)

    # return auth_controller.get_user_by_email(email, credentials)

# def decorated_function_with_arguments(function_arg1, function_arg2):
#     print ("Я - декорируемая функция и я знаю только о своих аргументах: {0}"
#     " {1}".format(function_arg1, function_arg2))
