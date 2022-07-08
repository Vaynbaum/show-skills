from typing import Union

from fastapi import HTTPException
from db.abstract_database_handler import AbstractDatabaseHandler
from models.response_items import ResponseItems
from models.message_model import MessageModel
from models.user_model import UserModelInDB, UserModelResponse
from handlers.jwt_handler import JWTHandler


class UserController:
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__database_controller = database_controller
        self.__jwt_handler = JWTHandler()

    async def get_user_by_username(
        self, username: Union[str, None]
    ) -> Union[UserModelResponse, None]:
        """Получение пользователя по нику (username)"""
        if username != None:
            user = await self.__database_controller.get_user_by_username(username)
            return UserModelResponse(**user.dict())
        return None

    async def get_user_by_key(
        self, key: Union[str, None]
    ) -> Union[UserModelInDB, None]:
        """Получение пользователя по ключу"""
        if key is not None:
            return await self.__database_controller.get_user_by_key(key)
        raise HTTPException(status_code=400, detail="Key is empty")

    async def get_user_all(
        self, limit, last_user_key
    ) -> ResponseItems[UserModelResponse]:
        """Получение всех пользователей"""
        return await self.__database_controller.get_user_all(
            limit if limit else None, last_user_key if last_user_key else None
        )

    async def delete_user_by_key(self, key: str) -> MessageModel:
        """Удаление пользователя из базы данных"""
        await self.__database_controller.delete_user_by_key(key)
        return MessageModel(message="Deletion successful")

    async def get_user_by_token(self, token):
        """Получение пользователя из бд по ключу из токена"""
        sub = self.__jwt_handler.decode_token(token)
        user = await self.__database_controller.get_user_by_key(sub)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid user key")
        return user
