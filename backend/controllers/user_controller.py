from fastapi.security import HTTPAuthorizationCredentials
from db.database_handler import DatabaseHandler

from handlers.jwt_handler import JWTHandler


class UserController():
    def __init__(self):
        self.__jwt_handler = JWTHandler()
        self.__database_controller = DatabaseHandler()

    def get_user_by_email(self, username: str, credentials: HTTPAuthorizationCredentials):
        token = credentials.credentials
        if(self.__jwt_handler.decode_token(token)):
            return self.__database_controller.get_user_by_username(username)