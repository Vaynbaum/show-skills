from typing import Union
from deta import Deta

from models.response_items import ResponseItems
from models.role_model import RoleInDBModel


class RoleDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__roles_db = deta.AsyncBase("roles")

    async def get_one_by_query(self, query: dict = None) -> Union[RoleInDBModel, None]:
        """Get one role by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.

        Returns:
            Union[RoleInDBModel, None]: If a role is found, then returns RoleInDBModel otherwise None
        """
        res_fetch = await self.__roles_db.fetch(query, limit=1)
        if res_fetch.count > 0:
            role_dict = res_fetch.items[0]
            return RoleInDBModel(**role_dict)
        else:
            None

    async def get_by_key(self, key: str) -> Union[RoleInDBModel, None]:
        """Get a role by key from the database

        Args:
            key (str): The role key in the database

        Returns:
            Union[RoleInDBModel, None]: If a role is found, then returns RoleInDBModel otherwise None
        """
        role = await self.__roles_db.get(key)
        return RoleInDBModel(**role) if role is not None else None

    async def get_many_by_query(
        self, query: Union[dict, list] = None
    ) -> ResponseItems[RoleInDBModel]:
        """Get roles by different criteria from the database

        Args:
            query (Union[dict, list], optional): Choosing criteria. Defaults to None.

        Returns:
            ResponseItems[RoleInDBModel]: Query result
        """
        roles = await self.__roles_db.fetch(query)
        print(roles)
        return ResponseItems[RoleInDBModel](
            count=roles.count, last=roles.last, items=roles.items
        )
