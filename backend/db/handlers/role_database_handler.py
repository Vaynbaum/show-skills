from typing import Union
from deta import Deta
from models.response_items import ResponseItems

from models.role_model import RoleModelInDB


class RoleDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__roles_db = deta.AsyncBase("roles")

    async def get_one_by_query(self, query: dict = None) -> Union[RoleModelInDB, None]:
        """Get one role by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.

        Returns:
            Union[RoleModelInDB, None]: If a role is found, then returns RoleModelInDB otherwise None
        """
        res_fetch = await self.__roles_db.fetch(query, limit=1)
        if res_fetch.count > 0:
            role_dict = res_fetch.items[0]
            return RoleModelInDB(**role_dict)
        else:
            None

    async def get_by_key(self, key: str) -> Union[RoleModelInDB, None]:
        """Get a role by key from the database

        Args:
            key (str): The role key in the database

        Returns:
            Union[RoleModelInDB, None]: If a role is found, then returns RoleModelInDB otherwise None
        """
        role = await self.__roles_db.get(key)
        return RoleModelInDB(**role) if role is not None else None

    async def get_many_by_query(
        self, query: dict = None, limit: int = 1000, last_role_key: str = None
    ) -> ResponseItems[RoleModelInDB]:
        """Get roles by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.
            limit (int, optional): Limit of roles received. Defaults to 1000.
            last_role_key (str, optional): The last role key received in the previous request. Defaults to None.

        Returns:
            ResponseItems[RoleModelInDB]: Query result
        """
        roles = await self.__roles_db.fetch(query, limit, last_role_key)
        return ResponseItems[RoleModelInDB](
            count=roles.count, last=roles.last, items=roles.items
        )
