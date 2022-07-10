from consts.name_roles import USER
from db.abstract_database_handler import AbstractDatabaseHandler
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from handlers.jwt_handler import JWTHandler
from handlers.password_handler import PasswordHandler
from models.message_model import MessageModel
from models.role_model import RoleModelResponse
from models.token_model import AccessTokenModel, PairTokenModel
from models.user_model import AuthModel, SignupModel, UserInDBModel


class AuthController:
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__database_controller = database_controller
        self.__password_handler = PasswordHandler()
        self.__jwt_handler = JWTHandler()

    async def signup(self, user_details: SignupModel):
        """Регистрация пользователя"""
        user = await self.__database_controller.get_user_by_email(user_details.email)
        if user != None:
            return MessageModel(message="Account already exists")
        user = await self.__database_controller.get_user_by_username(
            user_details.username
        )
        if user != None:
            return MessageModel(message="Username is already occupied")

        try:
            hashed_password = self.__password_handler.encode_password(
                user_details.password
            )
            role = await self.__database_controller.get_role_by_name_en(USER)

            user = UserInDBModel(
                email=user_details.email,
                username=user_details.username,
                password=hashed_password,
                lastname=user_details.lastname,
                firstname=user_details.firstname,
                role_key=role.key if (role is not None) else None,
                role=RoleModelResponse(**role.dict()) if (role is not None) else None,
                subscriptions=[],
                followers=[],
                links=[],
                skills=[],
            )
            await self.__database_controller.create_user(user)
            return MessageModel(message="Registration is successful")
        except:
            return MessageModel(message="Failed to signup user")

    async def login(self, user_details: AuthModel):
        """Аутенфикация пользователя"""
        user = await self.__database_controller.get_user_by_email(user_details.email)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email")
        if not self.__password_handler.verify_password(
            user_details.password, user.password
        ):
            raise HTTPException(status_code=401, detail="Invalid password")

        access_token = self.__jwt_handler.encode_token(user.key)
        refresh_token = self.__jwt_handler.encode_refresh_token(user.key)
        return PairTokenModel(access_token=access_token, refresh_token=refresh_token)

    def refresh_token(self, credentials: HTTPAuthorizationCredentials):
        """Создание нового access токена по refresh токену"""
        refresh_token = credentials.credentials
        new_token = self.__jwt_handler.refresh_token(refresh_token)
        return AccessTokenModel(access_token=new_token)
