from fastapi import HTTPException

from db.abstract_database_handler import AbstractDatabaseHandler
from exceptions.append_like_exception import AppendLikeException
from exceptions.update_post_exception import UpdatePostException
from handlers.jwt_handler import JWTHandler
from models.like_model import LikeModel
from models.message_model import MessageModel
from models.short_user_model_response import ShortUserModelResponse


class LikeController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__jwt_handler = JWTHandler()

    async def put_like(self, post_key: str, token: str) -> MessageModel:
        post = await self.__database_controller.get_post_by_key(post_key)
        if post is None:
            raise HTTPException(status_code=400, detail="Post not found")

        user_key = self.__jwt_handler.decode_token(token)
        result = list(filter(lambda item: user_key == item.user.key, post.likes))
        if len(result) > 0:
            raise HTTPException(status_code=400, detail="Like already put")

        user = await self.__database_controller.get_user_by_key(user_key)
        like = LikeModel(user=ShortUserModelResponse(**user.dict()))
        try:
            await self.__database_controller.append_like_to_post(like, post_key)
            return MessageModel(message="The like has been set successfully")
        except AppendLikeException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")

    async def remove_like(self, post_key: str, token: str) -> MessageModel:
        post = await self.__database_controller.get_post_by_key(post_key)
        if post is None:
            raise HTTPException(status_code=400, detail="Post not found")

        user_key = self.__jwt_handler.decode_token(token)
        result = list(filter(lambda item: user_key == item.user.key, post.likes))
        if len(result) == 0:
            raise HTTPException(status_code=400, detail="Like not found")

        post.likes.remove(result[0])
        try:
            await self.__database_controller.update_post_by_key(
                {"likes": (post.dict())["likes"]}, post_key
            )
            return MessageModel(message="Like successfully removed")
        except UpdatePostException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")
