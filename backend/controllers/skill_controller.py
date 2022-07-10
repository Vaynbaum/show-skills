from typing import Union
from fastapi import HTTPException, UploadFile
from transliterate import translit
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv

from controllers.user_controller import UserController
from db.abstract_database_handler import AbstractDatabaseHandler
from exceptions.append_skills_exception import AppendSkillsException
from exceptions.get_photo_exception import GetPhotoException
from exceptions.update_user_data_exception import UpdateUserDataException
from exceptions.upload_photo_exception import UploadPhotoException
from models.response_items import ResponseItems
from models.message_model import MessageModel
from models.skill_model import SkillCreateDataModel, SkillInDBModel
from drive.abstract_drive_handler import AbstractDriveHandler


class SkillController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
        driver_controller: AbstractDriveHandler,
    ):
        load_dotenv()
        self.__database_controller = database_controller
        self.__driver_controller = driver_controller
        self.__user_controller = UserController(database_controller)
        self.__directory = "skill/icon"
        self.__url = os.getenv("URL")


    async def create_skill(
        self, skill: SkillCreateDataModel
    ) -> Union[SkillInDBModel, None]:
        """Добавление нового навыка в базу данных"""
        return await self.__database_controller.create_skill(skill)

    def upload_icon_skill(self, name: str, file: UploadFile) -> str:
        """Загрузка иконки навыка на диск"""
        name_icon = translit(name, "ru", reversed=True).lower()
        size_icon = 128
        name_icon = self.__driver_controller.join_file_name(file, name_icon)
        try:
            name = self.__driver_controller.upload_photo(
                name_icon, self.__directory, file, size_icon, size_icon
            )
            return f"{self.__url}/{name}"
        except UploadPhotoException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")

    def get_icon_by_name_file(self, name_file: str) -> Union[StreamingResponse, None]:
        """Получение иконки навыка по названию фотографии"""
        try:
            return self.__driver_controller.get_photo(self.__directory, name_file)
        except GetPhotoException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")

    async def get_skill_all(
        self, limit: int = 1000, last_user_key: str = None
    ) -> ResponseItems[SkillInDBModel]:
        """Получение всех навыков из базы данных"""
        return await self.__database_controller.get_skill_all(limit, last_user_key)

    async def add_skill(self, skill_key: str, token: str):
        user = await self.__user_controller.get_user_by_token(token)
        result = list(filter(lambda item: skill_key == item.key, user.skills))
        if len(result) > 0:
            raise HTTPException(status_code=400, detail="Skill already exists")

        skill = await self.__database_controller.get_skill_by_key(skill_key)
        if skill is None:
            raise HTTPException(status_code=400, detail="Skill not found")

        try:
            await self.__database_controller.append_skills_to_user(
                [skill.dict()], user.key
            )
            return MessageModel(message="Adding successfully")
        except AppendSkillsException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")

    async def remove_skill(self, skill_key: str, token: str):
        user = await self.__user_controller.get_user_by_token(token)
        result = list(filter(lambda item: skill_key == item.key, user.skills))
        if len(result) == 0:
            raise HTTPException(status_code=400, detail="Skill not found")

        user.skills.remove(result[0])
        try:
            await self.__database_controller.update_simple_data_to_user(
                {"skills": (user.dict())["skills"]}, user.key
            )
            return MessageModel(message="Skill successfully removed")
        except UpdateUserDataException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")
