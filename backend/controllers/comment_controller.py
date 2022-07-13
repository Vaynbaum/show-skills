from typing import List
from fastapi import HTTPException
from controllers.user_controller import UserController
from db.database_handler import DatabaseHandler
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
        database_controller: DatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)
        self.__generator_handler = GeneratorHandler()
        self.__datetime_handler = DatetimeHandler()

    def __generate_comment_key(self, comments: list[CommentModel]) -> str:
        """Creating a random key for comments

        Args:
            comments (list[CommentModel]): List of comments to the post

        Returns:
            str: Generated key
        """
        LENGTH_KEY = 12
        while True:
            key = self.__generator_handler.generate_random_combination(LENGTH_KEY)
            result = list(filter(lambda item: key == item.key, comments))

            if len(result) == 0:
                return key

    async def __get_post_by_key(self, post_key: str) -> PostInDBModel:
        """Getting a post from the database by the post key

        Args:
            post_key (str)

        Raises:
            HTTPException: If post in not found

        Returns:
            PostInDBModel: Post model
        """
        post = await self.__database_controller.get_post_by_key(post_key)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    def __get_comment_by_key(
        self, comment_key: str, post: PostInDBModel
    ) -> CommentModel:
        """Getting a comment from a post by the comment key

        Args:
            comment_key (str)
            post (PostInDBModel)

        Raises:
            HTTPException: If comment is not found

        Returns:
            CommentModel: comment model
        """
        result = list(filter(lambda item: comment_key == item.key, post.comments))
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Comment not found")
        return result[0]

    async def post_comment(
        self, comment: CommentInputModel, post_key: str, token: str
    ) -> CommentModel:
        """Creating a comment

        Args:
            comment (CommentInputModel): comment model
            post_key (str)
            token (str): access token

        Raises:
            HTTPException: If it is not successful to add comment to the post

        Returns:
            CommentModel
        """
        post = await self.__get_post_by_key(post_key)
        user = await self.__user_controller.get_user_by_token(token)
        key = self.__generate_comment_key(post.comments)
        comment = CommentModel(
            **comment.dict(),
            author=ShortUserModelResponse(**user.dict()),
            number_comment=key,
            date_create=self.__datetime_handler.now(),
        )

        try:
            await self.__database_controller.append_comment_to_post(comment, post_key)
            return comment
        except AppendCommentException as e:
            raise HTTPException(status_code=400, detail=f"{e}")

    async def get_author_key_by_comment_key(
        self, comment_key: str, post_key: str
    ) -> str:
        """_summary_

        Args:
            comment_key (str)
            post_key (str)

        Returns:
            str: Received user key
        """        
        post = await self.__get_post_by_key(post_key)
        comment = self.__get_comment_by_key(comment_key, post)
        return comment.author.key

    async def delete_comment(
        self, comment_key: str, post_key: str
    ) -> List[CommentModel]:
        """Deleting a comment to a post

        Args:
            comment_key (str)
            post_key (str)

        Raises:
            HTTPException: If the comment to the post failed to delete

        Returns:
            List[CommentModel]
        """        
        post = await self.__get_post_by_key(post_key)
        comment = self.__get_comment_by_key(comment_key, post)
        post.comments.remove(comment)

        try:
            await self.__database_controller.update_post_by_key(
                {"comments": (post.dict())["comments"]}, post_key
            )
            return post.comments
        except UpdatePostException as e:

            raise HTTPException(status_code=400, detail=f"{e}")
