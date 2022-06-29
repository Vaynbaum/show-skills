from deta import Deta

from db.models.user_model import AbstractUserModelInDB


class UserDetaDetaDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__users_db = deta.Base('users')

    # def get_user_by_email(self, email: str):
    #     '''Получение одного пользователя по email из базы данных'''
    #     res_fetch = self.__users_db.fetch(
    #         {"email": email}, limit=1)
    #     return res_fetch.items[0] if len(res_fetch.items) > 0 else None

    def get_user_by_field(self, value: str, field: str):
        '''Получение одного пользователя по определенному полю из базы данных'''
        res_fetch = self.__users_db.fetch(
            {field: value}, limit=1)
        return res_fetch.items[0] if len(res_fetch.items) > 0 else None

    def create_user(self, user: AbstractUserModelInDB):
        '''Добавление пользователя в базу данных'''
        return self.__users_db.put(user.dict())
