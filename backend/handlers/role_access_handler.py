from typing import Union
from fastapi import HTTPException
from controllers.user_controller import UserController

from db.abstract_database_handler import AbstractDatabaseHandler
from models.user_model import UserModelInDB
from models.role_access_model import RoleAccessModel


class AccessHandler:
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__user_controller = UserController(database_controller)

    def __find_access_role(
        self, roles: list[RoleAccessModel], user: Union[UserModelInDB, None]
    ):
        """Проверка возможности доступа пользователя"""
        result = list(filter(lambda item: user.role.name_en in item.name, roles))
        if len(result) == 0:
            raise HTTPException(status_code=400, detail="No access")
        else:
            return result[0]

    def __clean_temp_vars(self, is_lact_decorator, kwargs):
        if is_lact_decorator:
            del kwargs["role"]
            del kwargs["user"]
        return kwargs

    async def __find_user(self, kwargs, token: str = None):
        if ("user" in kwargs) and kwargs["user"] is not None:
            user = kwargs["user"]
        elif token is not None:
            user = await self.__user_controller.get_user_by_token(token)
            kwargs["user"] = user
        else:
            raise HTTPException(status_code=400, detail="No access")
        return user, kwargs

    def __find_role(self, kwargs, user, roles: list[RoleAccessModel] = None):
        if "role" in kwargs and kwargs["role"] is not None:
            role = kwargs["role"]
        else:
            role = self.__find_access_role(roles, user)
            kwargs["role"] = role
        return role, kwargs

    def maker_role_access(
        self,
        token: str = None,
        roles: list[RoleAccessModel] = None,
        is_lact_decorator: bool = True,
    ):
        """Создание декоратора доступа пользователя по роли"""

        def decorator_role_access(func):
            """Декоратор"""

            async def wrapped_role_access(*args, **kwargs):
                """Обёртка"""
                user, kwargs = await self.__find_user(kwargs, token)
                role, kwargs = self.__find_role(kwargs, user, roles)
                # Если роль пользователя имеет доступ к функции, то вызываем ее
                if role is not None:
                    kwargs = self.__clean_temp_vars(is_lact_decorator, kwargs)
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(status_code=400, detail="No access")

            return wrapped_role_access

        return decorator_role_access

    def maker_owner_access(
        self,
        key_author: str,
        token: str = None,
        roles: list[RoleAccessModel] = None,
        is_lact_decorator: bool = True,
    ):
        """Создание декоратора доступа пользователя, на основе принадлежности объекта"""

        def decorator_owner_access(func):
            """Декоратор"""

            async def wrapped_owner_access(*args, **kwargs):
                """Обёртка"""
                user, kwargs = await self.__find_user(kwargs, token)
                role, kwargs = self.__find_role(kwargs, user, roles)
                # Если роль пользователя имеет доступ к функции, то вызываем ее
                if role.check_owner_access(user, key_author):
                    kwargs = self.__clean_temp_vars(is_lact_decorator, kwargs)
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(status_code=400, detail="No access")

            return wrapped_owner_access

        return decorator_owner_access
