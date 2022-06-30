from deta import Deta
from db.models.role_model import RoleModel

from db.models.user_model import UserModelInDB


class RoleDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__roles_db = deta.Base('roles')

    def get_role_by_name_en(self, title: str) -> RoleModel | None:
        '''Получение одной роли по названию на английском из базы данных'''
        res_fetch = self.__roles_db.fetch(
            {"name_en": title}, limit=1)
        return res_fetch.items[0] if res_fetch.count > 0 else None

    def get_role_by_key(self, key: str) -> RoleModel | None:
        '''Получение роли по ключу из базы данных'''
        return self.__roles_db.get(key)

    # def create_user(self, user: UserModelInDB):
    #     '''Добавление пользователя в базу данных'''
    #     return self.__users_db.put(user.dict())
