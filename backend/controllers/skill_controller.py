from typing import Union
from fastapi import UploadFile
from transliterate import translit
from fastapi.responses import HTMLResponse, StreamingResponse

from db.abstract_database_handler import AbstractDatabaseHandler
from models.items import ResponseItems
from models.skill_model import SkillCreateDataModel, SkillModelInDB
from drive.abstract_drive_handler import AbstractDriveHandler


class SkillController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
        driver_controller: AbstractDriveHandler,
    ):
        self.__database_controller = database_controller
        self.__driver_controller = driver_controller

    async def create_skill(
        self, skill: SkillCreateDataModel
    ) -> Union[SkillModelInDB, None]:
        """Добавление нового навыка в базу данных"""
        return await self.__database_controller.create_skill(skill)

    def upload_icon_skill(self, name, file: UploadFile) -> str:
        """Загрузка иконки навыка на диск"""
        name_icon = translit(name, "ru", reversed=True).lower()
        size_icon = 128
        return self.__driver_controller.upload_photo(
            name_icon, "skill/icon", file, size_icon, size_icon
        )

    def get_icon_by_name_file(self, name_file) -> Union[StreamingResponse, None]:
        """Получение иконки навыка по названию фотографии"""
        return self.__driver_controller.get_photo("skill/icon", name_file)

    async def get_skill_all(
        self, limit=100, last_user_key=None
    ) -> ResponseItems[SkillModelInDB]:
        """Получение всех навыков из базы данных"""
        return await self.__database_controller.get_skill_all(limit, last_user_key)
