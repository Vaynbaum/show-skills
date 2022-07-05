from typing import Union
from deta import Deta

from models.user_model import UserModelInDB


class UserDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__users_db = deta.AsyncBase("users")

    async def get_by_field(self, value: str, field: str) -> Union[UserModelInDB, None]:
        """Получение одного пользователя по определенному полю из базы данных"""
        res_fetch = await self.__users_db.fetch({field: value}, limit=1)
        return res_fetch.items[0] if res_fetch.count > 0 else None

    async def get_all(self, limit, last_user_key):
        """Получение всех пользователей"""
        return await self.__users_db.fetch(limit=limit, last=last_user_key)

    async def get_by_query(self, query, limit, last_user_key):
        """Получение пользователей по запросу"""
        return await self.__users_db.fetch(query)

    async def create(self, user: UserModelInDB) -> Union[UserModelInDB, None]:
        """Добавление пользователя в базу данных"""
        return await self.__users_db.put(user.dict())

    async def get_by_key(self, key: str) -> Union[UserModelInDB, None]:
        """Получение пользователя по ключу из базы данных"""
        return await self.__users_db.get(key)

    async def delete_by_key(self, key: str) -> None:
        """Удаление пользователя из базы данных по ключу"""
        return await self.__users_db.delete(key)

    async def put_many(self, users: list):
        return await self.__users_db.put_many(users)

    async def append_links(self, links: list, key: str) -> None:
        return await self.__users_db.update(
            {"links": self.__users_db.util.append(links)}, key
        )

    async def update_simple_data(self, data: dict, key: str) -> None:
        return await self.__users_db.update(data, key)
