from consts.name_roles import USER
from db.database_handler import DatabaseHandler
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from exceptions.refresh_token_exception import RefreshTokenException
from handlers.jwt_handler import JWTHandler
from handlers.password_handler import PasswordHandler
from models.message_model import MessageModel
from models.role_model import RoleModelResponse
from models.token_model import AccessTokenModel, PairTokenModel
from models.user_model import AuthModel, SignupModel, UserInDBModel


class AuthController:
    def __init__(self, database_controller: DatabaseHandler):
        self.__database_controller = database_controller
        self.__password_handler = PasswordHandler()
        self.__jwt_handler = JWTHandler()

    async def signup(self, user_details: SignupModel) -> MessageModel:
        """User registration

        Args:
            user_details (SignupModel): User model at registration

        Raises:
            HTTPException: If the email or password is already taken or failed to register

        Returns:
            MessageModel
        """
        user = await self.__database_controller.get_user_by_email(user_details.email)
        if user != None:
            raise HTTPException(status_code=401, detail="Account already exists")

        user = await self.__database_controller.get_user_by_username(
            user_details.username
        )
        if user != None:
            raise HTTPException(status_code=401, detail="Username is already used")
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
            result = await self.__database_controller.create_user(user)
            if result is None:
                raise HTTPException(status_code=401, detail="Failed to signup user")
            return MessageModel(message="Registration is successful")
        except:
            raise HTTPException(status_code=401, detail="Failed to signup user")

    async def login(self, user_details: AuthModel) -> PairTokenModel:
        """User authentication

        Args:
            user_details (AuthModel): User model at authorization

        Raises:
            HTTPException: If the password or login is invalid

        Returns:
            PairTokenModel: A pair of access and refresh tokens
        """
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

    def refresh_token(
        self, credentials: HTTPAuthorizationCredentials
    ) -> AccessTokenModel:
        """Creating a new access token by refresh token

        Args:
            credentials (HTTPAuthorizationCredentials)

        Raises:
            HTTPException: If the refresh token is invalid, expired or scope is invalid

        Returns:
            AccessTokenModel
        """
        try:
            new_token = self.__jwt_handler.refresh_token(credentials.credentials)
            return AccessTokenModel(access_token=new_token)
        except RefreshTokenException as e:
            
            raise HTTPException(status_code=401, detail=f"{e}")
