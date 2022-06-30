import os
from deta import Deta
from deta.base import FetchResponse
from dotenv import load_dotenv
from db.abstract_database_handler import AbstractDatabaseHandler
from db.handlers.role_database_handler import RoleDatabaseHandler

from db.handlers.user_database_handler import UserDatabaseHandler
from db.models.role_model import RoleModel
from db.models.user_model import UserModelInDB, UserResponseModel


class DatabaseHandler(AbstractDatabaseHandler):
    def __init__(self):
        load_dotenv()
        self.__deta = Deta(os.getenv('DETA_PROJECT_KEY'))
        self.__user_handler = UserDatabaseHandler(self.__deta)
        self.__role_handler = RoleDatabaseHandler(self.__deta)

    def get_user_by_email(self, email: str):
        return self.__user_handler.get_user_by_field(email, "email")

    def get_user_by_username(self, username: str):
        user = self.__user_handler.get_user_by_field(username, "username")
        if user is not None:
            return UserResponseModel(**user)
        return user

    def get_user_by_key(self, key: str):
        return self.__user_handler.get_user_by_key(key)

    def get_user_all(self, limit, last_user_key):
        '''Получение всех пользователей'''
        return self.__user_handler.get_user_all(limit, last_user_key)

    def create_user(self, user: UserModelInDB):
        return self.__user_handler.create_user(user)

    def delete_user_by_key(self, key: str):
        return self.__user_handler.delete_user_by_key(key)

    def get_role_by_name_en(self, title: str):
        return self.__role_handler.get_role_by_name_en(title)

    def get_role_by_key(self, key: str):
        return self.__role_handler.get_role_by_key(key)
