from deta import Deta
from deta.base import FetchResponse

from db.models.user_model import UserModelInDB, UserResponseModel


class UserDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__users_db = deta.Base('users')

    def get_user_by_field(self, value: str, field: str) -> UserModelInDB | None:
        '''Получение одного пользователя по определенному полю из базы данных'''
        res_fetch = self.__users_db.fetch(
            {field: value}, limit=1)
        return res_fetch.items[0] if res_fetch.count > 0 else None

    def get_user_all(self, limit, last_user_key):
        '''Получение всех пользователей'''
        return self.__users_db.fetch(limit=limit, last=last_user_key)

    def create_user(self, user: UserModelInDB) -> UserModelInDB | None:
        '''Добавление пользователя в базу данных'''
        return self.__users_db.put(user.dict())

    def get_user_by_key(self, key: str) -> UserModelInDB | None:
        '''Получение пользователя по ключу из базы данных'''
        return self.__users_db.get(key)

    def delete_user_by_key(self, key: str) -> None:
        '''Удаление пользователя из базы данных по ключу'''
        return self.__users_db.delete(key)
