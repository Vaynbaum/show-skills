from fastapi.security import HTTPAuthorizationCredentials

from db.abstract_database_handler import AbstractDetaDatabaseHandler
from db.deta_database_handler import DetaDatabaseHandler
from handlers.jwt_handler import JWTHandler


class UserController():
    def __init__(self):
        self.__jwt_handler = JWTHandler()
        self.__database_controller: AbstractDetaDatabaseHandler = DetaDatabaseHandler()

    def get_user_by_email(self, username: str):
        return self.__database_controller.get_user_by_username(username)

    def delete_user_by_key(self, key: str):
        pass

    # def get_user_by_email(self, username: str, credentials: HTTPAuthorizationCredentials):
    #     token = credentials.credentials
    #     if(self.__jwt_handler.decode_token(token)):
    #         return self.__database_controller.get_user_by_username(username)
