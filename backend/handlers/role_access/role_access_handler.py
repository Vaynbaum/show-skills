from typing import Union
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from controllers.user_controller import UserController

from db.abstract_database_handler import AbstractDatabaseHandler
from models.user_model import UserModelInDB
from handlers.role_access.role_access_model import RoleAccessModel


class AccessHandler:
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)

    def __find_access_role(
        self, roles: list[RoleAccessModel], user: Union[UserModelInDB, None]
    ):
        """Проверка существования пользователя и его возможность доступа"""
        if user is not None:
            result = list(filter(lambda item: user.role.name_en in item.name, roles))
            return result[0]
        return None

    def __clean_temp_vars(self, is_lact_decorator, kwargs):
        if is_lact_decorator:
            del kwargs["role"]
            del kwargs["user"]
        return kwargs

    async def __find_user(
        self, kwargs, credentials: Union[HTTPAuthorizationCredentials, None] = None
    ):
        if ("user" in kwargs) and kwargs["user"] is not None:
            user = kwargs["user"]
        elif credentials is not None:
            user = await self.__user_controller.get_user_by_token(
                credentials.credentials
            )
            kwargs["user"] = user
        else:
            raise HTTPException(status_code=402, detail="No access")

        return user, kwargs

    def __find_role(
        self, kwargs, user, roles: Union[list[RoleAccessModel], None] = None
    ):
        if "role" in kwargs and kwargs["role"] is not None:
            role = kwargs["role"]
        else:
            role = self.__find_access_role(roles, user)
            if role is not None:
                kwargs["role"] = role
            else:
                raise HTTPException(status_code=402, detail="No access")
        return role, kwargs

    def maker_role_access(
        self,
        credentials: Union[HTTPAuthorizationCredentials, None] = None,
        roles: Union[list[RoleAccessModel], None] = None,
        is_lact_decorator: bool = True,
    ):
        """Создание декоратора доступа пользователя по роли"""

        def decorator_role_access(func):
            """Декоратор"""

            async def wrapped_role_access(*args, **kwargs):
                """Обёртка"""
                user, kwargs = await self.__find_user(kwargs, credentials)
                role, kwargs = self.__find_role(kwargs, user, roles)
                # Если роль пользователя имеет доступ к функции, то вызываем ее
                if role is not None:
                    kwargs = self.__clean_temp_vars(is_lact_decorator, kwargs)
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(status_code=402, detail="No access")

            return wrapped_role_access

        return decorator_role_access

    def maker_owner_access(
        self,
        key_author: str,
        credentials: Union[HTTPAuthorizationCredentials, None] = None,
        roles: Union[list[RoleAccessModel], None] = None,
        is_lact_decorator: bool = True,
    ):
        """Создание декоратора доступа пользователя, на основе принадлежности объекта"""

        def decorator_owner_access(func):
            """Декоратор"""

            async def wrapped_owner_access(*args, **kwargs):
                """Обёртка"""
                user, kwargs = await self.__find_user(kwargs, credentials)
                role, kwargs = self.__find_role(kwargs, user, roles)
                # Если роль пользователя имеет доступ к функции, то вызываем ее
                if role.check_owner_access(user, key_author):
                    kwargs = self.__clean_temp_vars(is_lact_decorator, kwargs)
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(status_code=402, detail="No access")

            return wrapped_owner_access

        return decorator_owner_access
