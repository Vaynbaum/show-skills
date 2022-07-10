from typing import Union
from fastapi import HTTPException
from controllers.user_controller import UserController

from db.abstract_database_handler import AbstractDatabaseHandler
from exceptions.no_roles_access_handler import NoRolesAccessHandler
from exceptions.no_token_access_handler import NoTokenAccessHandler
from models.user_model import UserInDBModel
from models.role_access_model import RoleAccessModel


class AccessHandler:
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__user_controller = UserController(database_controller)
        self.__database_controller = database_controller

    def __find_access_role(
        self, roles: list[RoleAccessModel], user: UserInDBModel
    ) -> RoleAccessModel:
        """Find the user's role in the list with allowed roles

        Args:
            roles (list[RoleAccessModel]): role list
            user (UserInDBModel): user's database model

        Raises:
            HTTPException: if the user's role is not in the list of roles,
            the allowed method

        Returns:
            RoleAccessModel: role found from the list of allowed
        """
        result = list(filter(lambda item: user.role.name_en in item.name, roles))
        if len(result) == 0:
            raise HTTPException(
                status_code=403,
                detail="The user's role is not in the list of roles allowed method",
            )
        else:
            return result[0]

    def __clean_temp_vars(self, is_lact_decorator: bool, kwargs: dict) -> dict:
        """Clearing temporary values from kwargs

        Args:
            is_lact_decorator (bool): Flag whether to delete temporary values
            kwargs (dict)

        Returns:
            dict: Cleared kvargs
        """
        if is_lact_decorator:
            del kwargs["role"]
            del kwargs["user"]
        return kwargs

    async def __find_user(
        self, kwargs: dict, token: str = None
    ) -> tuple[UserInDBModel, dict]:
        """Get a user

        Args:
            kwargs (dict)
            token (str, optional): user's token. Defaults to None.

        Raises:
            NoTokenAccessHandler: If it was not possible to find get a user

        Returns:
            tuple[UserInDBModel, dict]: user model and kwargs
        """
        if ("user" in kwargs) and kwargs["user"] is not None:
            user = kwargs["user"]
        elif token is not None:
            user = await self.__user_controller.get_user_by_token(token)
            kwargs["user"] = user
        else:
            raise NoTokenAccessHandler("Failed to get the user")
        return user, kwargs

    def __find_role(
        self, kwargs: dict, user: UserInDBModel, roles: list[RoleAccessModel] = None
    ) -> tuple[RoleAccessModel, dict]:
        """Get a role

        Args:
            kwargs (dict)
            user (UserInDBModel): user's database model
            roles (list[RoleAccessModel], optional): role list. Defaults to None.

        Raises:
            NotRolesAccessHandler: If there is no list of roles

        Returns:
            tuple[RoleAccessModel, dict]: role model and kwargs
        """
        if "role" in kwargs and kwargs["role"] is not None:
            role = kwargs["role"]
        elif roles is not None:
            role = self.__find_access_role(roles, user)
            kwargs["role"] = role
        else:
            raise NoRolesAccessHandler("There is no list of roles")
        return role, kwargs

    async def __get_role_user_access(
        self, kwargs: dict, token: str = None, roles: list[RoleAccessModel] = None
    ) -> tuple[dict, UserInDBModel, RoleAccessModel]:
        """Get role and user

        Args:
            kwargs (dict)
            token (str, optional): user's token. Defaults to None.
            roles (list[RoleAccessModel], optional): role list. Defaults to None.

        Raises:
            HTTPException: If an error occurred while verifying access

        Returns:
            tuple[dict, UserInDBModel, RoleAccessModel]: kwargs, user model and role model
        """
        try:
            user, kwargs = await self.__find_user(kwargs, token)
        except NoTokenAccessHandler as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail="An error occurred while verifying access",
            )

        try:
            role, kwargs = self.__find_role(kwargs, user, roles)
        except NoRolesAccessHandler as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail="An error occurred while verifying access",
            )

        return kwargs, user, role

    def maker_role_access(
        self,
        token: str = None,
        roles: list[RoleAccessModel] = None,
        is_lact_decorator: bool = True,
    ):
        """Creating a user access decorator by role"""

        def decorator_role_access(func):
            async def wrapped_role_access(*args, **kwargs):
                kwargs, user, role = await self.__get_role_user_access(
                    kwargs, token, roles
                )
                # If the role is found, then call method
                if role is not None:
                    kwargs = self.__clean_temp_vars(is_lact_decorator, kwargs)
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(
                        status_code=403, detail="There is no access to this method"
                    )

            return wrapped_role_access

        return decorator_role_access

    def maker_owner_access(
        self,
        author_key: str,
        token: str = None,
        roles: list[RoleAccessModel] = None,
        is_lact_decorator: bool = True,
    ):
        """Creating a user access decorator by object ownership"""

        def decorator_owner_access(func):
            async def wrapped_owner_access(*args, **kwargs):
                kwargs, user, role = await self.__get_role_user_access(
                    kwargs, token, roles
                )
                # If the user's role allows action on the object, then call method
                if role.check_owner_access(user, author_key):
                    kwargs = self.__clean_temp_vars(is_lact_decorator, kwargs)
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(
                        status_code=403, detail="There is no access to this method"
                    )

            return wrapped_owner_access

        return decorator_owner_access

    def maker_assign_access(
        self,
        to_user_key: str,
        token: str = None,
        roles: list[RoleAccessModel] = None,
        is_lact_decorator: bool = True,
    ):
        """Creating a user access decorator, if possible assign"""

        def decorator_assign_access(func):
            async def wrapped_assign_access(*args, **kwargs):
                kwargs, user, role = await self.__get_role_user_access(
                    kwargs, token, roles
                )
                to_user = await self.__database_controller.get_user_by_key(to_user_key)
                if to_user is None:
                    raise HTTPException(status_code=400, detail="User not found")
                # If the user role allows you to assign a user, then call the method
                if role.check_to_user(to_user):
                    kwargs = self.__clean_temp_vars(is_lact_decorator, kwargs)
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(
                        status_code=403, detail="There is no access to this method"
                    )

            return wrapped_assign_access

        return decorator_assign_access
