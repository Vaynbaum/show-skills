from fastapi.security import HTTPAuthorizationCredentials
from db.abstract_database_handler import AbstractDatabaseHandler

from db.database_handler import DatabaseHandler
from handlers.jwt_handler import JWTHandler


class UserController():
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__jwt_handler = JWTHandler()
        self.__database_controller = database_controller

    def get_user_by_username(self, username: str | None):
        '''Получение пользователя по нику (username)'''
        if username != None:
            return self.__database_controller.get_user_by_username(username)
        return None

    def get_user_by_key(self, key: str | None):
        '''Получение пользователя по ключу'''
        if key != None:
            return self.__database_controller.get_user_by_username(key)
        return {"message": "Key is empty"}

    def get_user_all(self, limit=100, last_user_key=None):
        '''Получение всех пользователей'''
        return self.__database_controller.get_user_all(limit, last_user_key)

    def delete_user_by_key(self, key: str | None):
        '''Удаление пользователя из базы данных'''
        if key != None:
            self.__database_controller.delete_user_by_key(key)
            return {"message": "Deletion successful"}
        return {"message": "Key is empty"}

    # def get_user_by_email(self, username: str, credentials: HTTPAuthorizationCredentials):
    #     token = credentials.credentials
    #     if(self.__jwt_handler.decode_token(token)):
    #         return self.__database_controller.get_user_by_username(username)
