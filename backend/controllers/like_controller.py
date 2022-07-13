from typing import List
from fastapi import HTTPException

from db.database_handler import DatabaseHandler
from exceptions.append_like_exception import AppendLikeException
from exceptions.update_post_exception import UpdatePostException
from handlers.jwt_handler import JWTHandler
from models.like_model import LikeModel
from models.message_model import MessageModel
from models.short_user_model_response import ShortUserModelResponse


class LikeController:
    def __init__(
        self,
        database_controller: DatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__jwt_handler = JWTHandler()

    async def put_like(self, post_key: str, token: str) -> MessageModel:
        """Like the post

        Args:
            post_key (str)
            token (str): access token

        Raises:
            HTTPException: If post is not found, the like has already been set or
            it failed to put a like

        Returns:
            MessageModel
        """
        post = await self.__database_controller.get_post_by_key(post_key)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")

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
            raise HTTPException(status_code=400, detail=f"{e}")

    async def remove_like(self, post_key: str, token: str) -> List[LikeModel]:
        """Remove the like to the post

        Args:
            post_key (str)
            token (str): access token

        Raises:
            HTTPException: If the post or like is not found or
            it is not successful to remove the like

        Returns:
            List[LikeModel]: Remaining likes
        """        
        post = await self.__database_controller.get_post_by_key(post_key)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")

        user_key = self.__jwt_handler.decode_token(token)
        result = list(filter(lambda item: user_key == item.user.key, post.likes))
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Like not found")

        post.likes.remove(result[0])
        try:
            await self.__database_controller.update_post_by_key(
                {"likes": (post.dict())["likes"]}, post_key
            )
            return post.likes
        except UpdatePostException as e:

            raise HTTPException(status_code=400, detail=f"{e}")
