from typing import Union
from deta import Deta

from exceptions.update_item_exception import UpdateItemException
from models.comment_model import CommentModel
from models.like_model import LikeModel
from models.post_model import PostInDBModel, PostInputModel
from models.response_items import ResponseItems


class PostDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__posts_db = deta.AsyncBase("posts")

    async def create(self, post: PostInDBModel) -> Union[PostInDBModel, None]:
        """Adding a new post to the database

        Args:
            post (PostInDBModel): New post model

        Returns:
            Union[PostInDBModel, None]: The model of the post added to the database otherwise None
        """
        try:
            post = await self.__posts_db.put(post.dict())
            return PostInDBModel(**post)
        except:
            return None

    async def get_many_by_query(
        self, query: dict = None, limit: int = 1000, last_post_key: str = None
    ) -> ResponseItems[PostInDBModel]:
        """Get posts by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.
            limit (int, optional): Limit of posts received. Defaults to 1000.
            last_post_key (str, optional): The last post key received in the previous request.
            Defaults to None.

        Returns:
            ResponseItems[PostInDBModel]: Query result
        """
        result = await self.__posts_db.fetch(query, limit=limit, last=last_post_key)
        return ResponseItems[PostInDBModel](
            count=result.count, last=result.last, items=result.items
        )

    async def get_by_key(self, key: str) -> Union[PostInDBModel, None]:
        post = await self.__posts_db.get(key)
        return PostInDBModel(**post) if post is not None else None

    async def delete_by_key(self, key: str) -> None:
        return await self.__posts_db.delete(key)

    async def update(self, post: dict, key: str) -> None:
        """Updating of post data

        Args:
            post (dict): post data
            key (str): The post key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__posts_db.update(post, key)
        except BaseException as e:
            print(e)
            raise UpdateItemException("Updating data was not successful")

    async def append_like(self, like: LikeModel, post_key: str) -> None:
        """Add like to post

        Args:
            like (LikeModel): like model
            post_key (str): post key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__posts_db.update(
                {"likes": self.__posts_db.util.append(like.dict())}, post_key
            )
        except BaseException as e:
            print(e)
            raise UpdateItemException("Updating data was not successful")

    async def append_comment(self, comment: CommentModel, post_key: str) -> None:
        """Add comment to post

        Args:
            comment (CommentModel): like model
            post_key (str): post key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__posts_db.update(
                {"comments": self.__posts_db.util.append(comment.dict())}, post_key
            )
        except BaseException as e:
            print(e)
            raise UpdateItemException("Updating data was not successful")
