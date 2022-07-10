from typing import Union
from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv

from controllers.user_controller import UserController
from db.abstract_database_handler import AbstractDatabaseHandler
from drive.abstract_drive_handler import AbstractDriveHandler
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
        database_controller: AbstractDatabaseHandler,
        driver_controller: AbstractDriveHandler,
    ):
        load_dotenv()
        self.__database_controller = database_controller
        self.__driver_controller = driver_controller
        self.__user_controller = UserController(database_controller)
        self.__generator_handler = GeneratorHandler()
        self.__directory = "post/photo"
        self.__url = os.getenv("URL")
        self.__datetime_handler = DatetimeHandler()

    async def create_post(
        self, post: PostInputModel, token: str
    ) -> Union[PostInDBModel, None]:
        user = await self.__user_controller.get_user_by_token(token)
        post = PostInDBModel(
            **post.dict(),
            date_create=self.__datetime_handler.now(),
            author=ShortUserModelResponse(**user.dict()),
            author_key=user.key,
            likes=list(),
            comments=list(),
        )
        return await self.__database_controller.create_post(post)

    def upload_photo(self, file: UploadFile) -> str:
        rand_str = self.__generator_handler.generate_random_combination(8)
        name_file = f"{rand_str}_{file.filename}"
        try:
            name = self.__driver_controller.upload_photo(
                name_file, self.__directory, file
            )
            return f"{self.__url}/{name}"
        except UploadPhotoException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")

    def get_photo(self, name_image: str) -> Union[StreamingResponse, None]:
        try:
            return self.__driver_controller.get_photo(self.__directory, name_image)
        except GetPhotoException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")

    async def get_all_post(
        self, limit: int = 1000, last_post_key: str = None
    ) -> ResponseItems[PostInDBModel]:
        return await self.__database_controller.get_all_posts(limit, last_post_key)

    async def get_posts_by_skill(
        self, name_skill: str, limit: int = 1000, last_post_key: str = None
    ) -> ResponseItems[PostInDBModel]:
        return await self.__database_controller.get_posts_by_skill(
            name_skill, limit, last_post_key
        )

    async def delete_post_by_key(self, key: str) -> MessageModel:
        await self.__database_controller.delete_post_by_key(key)
        return MessageModel(message="Deletion successful")

    async def get_author_key_by_post_key(self, post_key: str) -> str:
        post = await self.__database_controller.get_post_by_key(post_key)
        if post is None:
            raise HTTPException(status_code=400, detail="Event not found")
        return post.author_key

    async def update_post(self, post: PostInputModel, post_key: str):
        try:
            await self.__database_controller.update_post_by_key(post.dict(), post_key)
            return MessageModel(message="Editing successful")
        except UpdatePostException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")
