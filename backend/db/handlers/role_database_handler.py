from typing import Union
from deta import Deta

from models.role_model import RoleModelInDB


class RoleDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__roles_db = deta.AsyncBase("roles")

    async def get_by_name_en(self, title: str) -> Union[RoleModelInDB, None]:
        """Получение одной роли по названию на английском из базы данных"""
        res_fetch = await self.__roles_db.fetch({"name_en": title}, limit=1)
        return res_fetch.items[0] if res_fetch.count > 0 else None

    async def get_by_key(self, key: str) -> Union[RoleModelInDB, None]:
        """Получение роли по ключу из базы данных"""
        return await self.__roles_db.get(key)
