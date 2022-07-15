from typing import Union

from fastapi import HTTPException
from db.database_handler import DatabaseHandler
from exceptions.decode_token_exception import DecodeTokenException
from exceptions.update_user_data_exception import UpdateUserDataException
from handlers.datetime_handler import DatetimeHandler
from models.response_items import ResponseItems
from models.message_model import MessageModel
from models.user_model import UserAdditionalDataModel, UserInDBModel, UserModelResponse
from handlers.jwt_handler import JWTHandler


class UserController:
    def __init__(self, database_controller: DatabaseHandler):
        self.__database_controller = database_controller
        self.__jwt_handler = JWTHandler()

    async def get_user_by_username(
        self, username: str
    ) -> Union[UserModelResponse, None]:
        """Getting a user by username

        Args:
            username (str): User's username

        Returns:
            Union[UserModelResponse, None]: If a user is found,
            then returns UserInDBModel otherwise None
        """
        user = await self.__database_controller.get_user_by_username(username)
        if user != None:
            return UserModelResponse(**user.dict())
        return None

    async def get_user_by_key(self, key: str) -> Union[UserInDBModel, None]:
        """Получение пользователя по ключу"""
        if key is not None:
            return await self.__database_controller.get_user_by_key(key)
        raise HTTPException(status_code=400, detail="Key is empty")

    async def get_user_all(
        self, limit: int, last_user_key: str
    ) -> ResponseItems[UserModelResponse]:
        """Getting all users

        Args:
            limit (int): Limit of users received
            last_user_key (str): The last user key received in the previous request

        Returns:
            ResponseItems[UserModelResponse]: Query result
        """
        return await self.__database_controller.get_user_all(limit, last_user_key)

    async def delete_user_by_key(self, key: str) -> MessageModel:
        """Deleting a user from the database

        Args:
            key (str): user's key

        Returns:
            MessageModel
        """
        await self.__database_controller.delete_user_by_key(key)
        return MessageModel(message="Deletion successful")

    async def get_user_by_token(self, token: str) -> UserInDBModel:
        """Getting a user from the database using a key from a token

        Args:
            token (str): access token

        Raises:
            HTTPException:  If the token is invalid, expired, scope is invalid
            or the user key is invalid

        Returns:
            UserInDBModel
        """
        try:
            sub = self.__jwt_handler.decode_token(token)
        except DecodeTokenException as e:

            raise HTTPException(status_code=401, detail=f"{e}")
        user = await self.__database_controller.get_user_by_key(sub)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid user key")
        return user

    async def update_additional_user_data_by_key(
        self, user: UserAdditionalDataModel, token: str
    ) -> MessageModel:
        """Changes to additional user data

        Args:
            user (UserAdditionalDataModel): User model for changing data
            token (str): access token

        Raises:
            HTTPException: If the token is invalid, expired, scope is invalid, invalid data
            or the user data update was not successful

        Returns:
            MessageModel
        """
        ALLOW_YEAR_LEFT = -100
        ALLOW_YEAR_RIGHT = -14
        datetime_handler = DatetimeHandler()

        birth_date = datetime_handler.convert_to_datetime(user.birth_date)
        if not datetime_handler.check_year_range(
            birth_date, ALLOW_YEAR_LEFT, ALLOW_YEAR_RIGHT
        ):
            raise HTTPException(status_code=400, detail="Invalid year")

        try:
            sub = self.__jwt_handler.decode_token(token)
        except DecodeTokenException as e:

            raise HTTPException(status_code=401, detail=f"{e}")
        try:
            await self.__database_controller.update_simple_data_to_user(
                user.dict(), sub
            )
            return MessageModel(message="Data successfully added")
        except UpdateUserDataException as e:

            raise HTTPException(status_code=400, detail=f"{e}")
