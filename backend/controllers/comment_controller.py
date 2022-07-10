from fastapi import HTTPException
from controllers.user_controller import UserController
from db.abstract_database_handler import AbstractDatabaseHandler
from exceptions.append_comment_exception import AppendCommentException
from exceptions.update_post_exception import UpdatePostException
from handlers.datetime_handler import DatetimeHandler
from handlers.generator_handler import GeneratorHandler
from models.comment_model import CommentInputModel, CommentModel
from models.message_model import MessageModel
from models.post_model import PostInDBModel
from models.short_user_model_response import ShortUserModelResponse


class CommentController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)
        self.__generator_handler = GeneratorHandler()
        self.__datetime_handler = DatetimeHandler()

    def __generate_comment_key(self, comments: list[CommentModel]) -> str:
        while True:
            key = self.__generator_handler.generate_random_combination(12)
            result = list(filter(lambda item: key == item.key, comments))

            if len(result) == 0:    
                return key

    async def __get_post_by_key(self, post_key: str) -> PostInDBModel:
        post = await self.__database_controller.get_post_by_key(post_key)
        if post is None:
            raise HTTPException(status_code=400, detail="Post not found")
        return post

    def __get_comment_by_key(
        self, comment_key: str, post: PostInDBModel
    ) -> CommentModel:
        result = list(filter(lambda item: comment_key == item.key, post.comments))
        if len(result) == 0:
            raise HTTPException(status_code=400, detail="Comment not found")
        return result[0]

    async def post_comment(
        self, comment: CommentInputModel, post_key: str, token: str
    ) -> MessageModel:
        post = await self.__get_post_by_key(post_key)
        user = await self.__user_controller.get_user_by_token(token)
        key = self.__generate_comment_key(post.comments)
        comment = CommentModel(
            **comment.dict(),
            author=ShortUserModelResponse(**user.dict()),
            number_comment=key,
            date_create = self.__datetime_handler.now()
        )

        try:
            await self.__database_controller.append_comment_to_post(comment, post_key)
            return MessageModel(message="The comment has been set successfully")
        except AppendCommentException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")

    async def get_author_key_by_comment_key(
        self, comment_key: str, post_key: str
    ) -> str:
        post = await self.__get_post_by_key(post_key)
        comment = self.__get_comment_by_key(comment_key, post)
        return comment.author.key

    async def delete_comment(self, comment_key: str, post_key: str) -> MessageModel:
        post = await self.__get_post_by_key(post_key)
        comment = self.__get_comment_by_key(comment_key, post)
        post.comments.remove(comment)

        try:
            await self.__database_controller.update_post_by_key(
                {"comments": (post.dict())["comments"]}, post_key
            )
            return MessageModel(message="Comment successfully removed")
        except UpdatePostException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")
