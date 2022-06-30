from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from db.abstract_database_handler import AbstractDatabaseHandler
from db.models.role_model import RoleDataModel, RoleModel
from db.models.user_model import AuthModel, UserModelInDB, SignupModel
from handlers.jwt_handler import JWTHandler
from handlers.password_handler import PasswordHandler


class AuthController():
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__database_controller = database_controller
        self.__password_handler = PasswordHandler()
        self.__jwt_handler = JWTHandler()

    def signup(self, user_details: SignupModel):
        '''Регистрация пользователя'''
        if self.__database_controller.get_user_by_email(user_details.email) != None:
            return {"message": "Account already exists"}
        try:
            hashed_password = self.__password_handler.encode_password(user_details.password)
            user_username = UserModelInDB.get_username_by_email(user_details.email)
            role = self.__database_controller.get_role_by_name_en("user")
            user = UserModelInDB(email=user_details.email, username=user_username, 
                                role=RoleDataModel(**role), password=hashed_password, 
                                lastname=user_details.lastname, firstname=user_details.firstname, 
                                role_key = role['key'])
            self.__database_controller.create_user(user)
            return {"message": "Registration is successful"}
        except:
            return {"message": 'Failed to signup user'}

    def login(self, user_details: AuthModel):
        '''Аутенфикация пользователя'''
        user: UserModelInDB = self.__database_controller.get_user_by_email(user_details.email)

        if (user is None):
            return HTTPException(status_code=401, detail='Invalid email')
        if (not self.__password_handler.verify_password(user_details.password, user['password'])):
            return HTTPException(status_code=401, detail='Invalid password')

        access_token = self.__jwt_handler.encode_token(user['key'])
        refresh_token = self.__jwt_handler.encode_refresh_token(user['key'])
        return {'access_token': access_token, 'refresh_token': refresh_token}

    def refresh_token(self, credentials: HTTPAuthorizationCredentials):
        '''Создание нового access токена по refresh токену'''
        refresh_token = credentials.credentials
        new_token = self.__jwt_handler.refresh_token(refresh_token)
        return {'access_token': new_token}
