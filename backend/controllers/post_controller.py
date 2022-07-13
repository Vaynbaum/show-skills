from typing import Union
from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv

from controllers.user_controller import UserController
from db.database_handler import DatabaseHandler
from handlers.drive_handler import DriveHandler
from exceptions.get_photo_exception import GetPhotoException
from exceptions.update_post_exception import UpdatePostException
from exceptions.upload_photo_exception import UploadPhotoException
from handlers.datetime_handler import DatetimeHandler
from handlers.generator_handler import GeneratorHandler
from models.message_model import MessageModel
from models.post_model import PostInDBModel, PostInputModel
from models.response_items import ResponseItems
from models.short_user_model_response import ShortUserModelResponse


class PostController:
    def __init__(
        self,
        database_controller: DatabaseHandler,
        driver_controller: DriveHandler,
    ):
        load_dotenv()
        self.__database_controller = database_controller
        self.__driver_controller = driver_controller
        self.__user_controller = UserController(database_controller)
        self.__generator_handler = GeneratorHandler()
        self.__directory = "post/photo"
        self.__url = os.getenv("URL")
        self.__datetime_handler = DatetimeHandler()

    async def create_post(self, post: PostInputModel, token: str) -> PostInDBModel:
        """Adding a new post to the database

        Args:
            post (PostInputModel): post input data
            token (str): access token

        Raises:
            HTTPException: If the post failed to add

        Returns:
            PostInDBModel: The model of the post added to the database
        """
        user = await self.__user_controller.get_user_by_token(token)
        post = PostInDBModel(
            **post.dict(),
            date_create=self.__datetime_handler.now(),
            author=ShortUserModelResponse(**user.dict()),
            likes=list(),
            comments=list(),
        )
        result = await self.__database_controller.create_post(post)
        if result is None:
            raise HTTPException(status_code=400, detail="Failed to add post")
        return result

    def upload_photo(self, file: UploadFile) -> str:
        """Uploading an image to disk

        Args:
            file (UploadFile)

        Raises:
            HTTPException: If the image format is invalid or the upload failed

        Returns:
            str: Photo URL
        """
        LENGTH_RAND_STR = 8
        rand_str = self.__generator_handler.generate_random_combination(LENGTH_RAND_STR)
        name_file = f"{rand_str}_{file.filename}"
        try:
            name = self.__driver_controller.upload_photo(
                name_file, self.__directory, file
            )
            return f"{self.__url}/{name}"
        except UploadPhotoException as e:

            raise HTTPException(status_code=400, detail=f"{e}")

    def get_photo(self, name_image: str) -> Union[StreamingResponse, None]:
        """Getting the photo by the name

        Args:
            name_image (str)

        Raises:
            HTTPException: If the file could not be retrieved

        Returns:
            Union[StreamingResponse, None]: The resulting image
        """
        try:
            return self.__driver_controller.get_photo(self.__directory, name_image)
        except GetPhotoException as e:

            raise HTTPException(status_code=400, detail=f"{e}")

    async def get_all_post(
        self, limit: int, last_post_key: str
    ) -> ResponseItems[PostInDBModel]:
        """Getting all posts from the database

        Args:
            limit (int): Limit of posts received
            last_post_key (str): The last post key received in the previous request

        Returns:
            ResponseItems[PostInDBModel]: Query result
        """
        return await self.__database_controller.get_posts_by_query(limit, last_post_key)

    async def get_posts_by_skill(
        self, name_skill: str, limit: int, last_post_key: str
    ) -> ResponseItems[PostInDBModel]:
        """Getting posts by skill name  from the database

        Args:
            name_skill (str)
            limit (int): Limit of posts received
            last_post_key (str): The last post key received in the previous request

        Returns:
            ResponseItems[PostInDBModel]: Query result
        """
        return await self.__database_controller.get_posts_by_query(
            limit, last_post_key, {"skill.name": name_skill}
        )

    async def delete_post_by_key(self, key: str) -> MessageModel:
        """Deleting a post

        Args:
            key (str): post key

        Returns:
            MessageModel
        """
        await self.__database_controller.delete_post_by_key(key)
        return MessageModel(message="Deletion successful")

    async def get_author_key_by_post_key(self, post_key: str) -> str:
        """Getting the post author's key

        Args:
            post_key (str)

        Raises:
            HTTPException: If the post is not found

        Returns:
            str: Post author's key
        """
        post = await self.__database_controller.get_post_by_key(post_key)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post.author.key

    async def update_post(self, post: PostInputModel, post_key: str) -> MessageModel:
        """Updating of post data

        Args:
            post (PostInputModel): Input post data

            post_key (str): 

        Raises:
            HTTPException: If the post data update was not successful

        Returns:
            MessageModel
        """
        try:
            await self.__database_controller.update_post_by_key(post.dict(), post_key)
            return MessageModel(message="Editing successful")
        except UpdatePostException as e:

            raise HTTPException(status_code=400, detail=f"{e}")
