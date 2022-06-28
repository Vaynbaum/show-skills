import os
from deta import Deta
from dotenv import load_dotenv

from db.handlers.user_database_handler import UserDatabaseHandler
from db.schemas.user_schema import AuthSchema, UserResponse, UserSchemaInDB


class DatabaseHandler():
    def __init__(self):
        load_dotenv()
        self.__deta = Deta(os.getenv('DETA_PROJECT_KEY'))
        self.__user_handler = UserDatabaseHandler(self.__deta)

    def get_user_by_email(self, email: str):
        '''Получение одного пользователя по email из базы данных'''
        return self.__user_handler.get_user_by_field(email, "email")

    def get_user_by_username(self, username: str):
        '''Получение одного пользователя по username из базы данных'''
        user = self.__user_handler.get_user_by_field(username, "username")
        if user is not None:
            return UserResponse(**user)
        return user

    def create_user(self, user: UserSchemaInDB):
        '''Добавление пользователя в базу данных'''
        return self.__user_handler.create_user(user)
