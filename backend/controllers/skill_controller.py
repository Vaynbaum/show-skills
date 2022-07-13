from typing import List, Union
from fastapi import HTTPException, UploadFile
from transliterate import translit
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv

from controllers.user_controller import UserController
from db.database_handler import DatabaseHandler
from exceptions.append_skills_exception import AppendSkillsException
from exceptions.get_photo_exception import GetPhotoException
from exceptions.update_user_data_exception import UpdateUserDataException
from exceptions.upload_photo_exception import UploadPhotoException
from models.response_items import ResponseItems
from models.message_model import MessageModel
from models.skill_model import SkillCreateDataModel, SkillInDBModel
from handlers.drive_handler import DriveHandler


class SkillController:
    def __init__(
        self,
        database_controller: DatabaseHandler,
        driver_controller: DriveHandler,
    ):
        load_dotenv()
        self.__database_controller = database_controller
        self.__driver_controller = driver_controller
        self.__user_controller = UserController(database_controller)
        self.__directory = "skill/icon"
        self.__url = os.getenv("URL")

    async def create_skill(self, skill: SkillCreateDataModel) -> SkillInDBModel:
        """Adding a new skill to the database

        Args:
            skill (SkillCreateDataModel): Skill input data

        Raises:
            HTTPException: If the skill failed to add

        Returns:
            SkillInDBModel: The model of the skill added to the database otherwise None
        """
        result = await self.__database_controller.create_skill(skill)
        if result is None:
            raise HTTPException(status_code=400, detail="Failed to add skill")
        return result

    def upload_icon_skill(self, name: str, file: UploadFile) -> str:
        """Uploading the skill icon to disk

        Args:
            name (str): file name
            file (UploadFile)

        Raises:
            HTTPException: If the image format is invalid or the upload failed

        Returns:
            str: Image URL
        """
        name_icon = translit(name, "ru", reversed=True).lower()
        size_icon = 128
        name_icon = self.__driver_controller.join_file_name(file, name_icon)
        try:
            name = self.__driver_controller.upload_photo(
                name_icon, self.__directory, file, size_icon, size_icon
            )
            return f"{self.__url}/{name}"
        except UploadPhotoException as e:

            raise HTTPException(status_code=400, detail=f"{e}")

    def get_icon_by_name_file(self, name_file: str) -> Union[StreamingResponse, None]:
        """Getting the skill icon by the name of the photo

        Args:
            name_file (str)

        Raises:
            HTTPException: If the file could not be retrieved

        Returns:
            Union[StreamingResponse, None]
        """
        try:
            return self.__driver_controller.get_photo(self.__directory, name_file)
        except GetPhotoException as e:

            raise HTTPException(status_code=400, detail=f"{e}")

    async def get_skill_all(
        self, limit: int, last_skill_key: str
    ) -> ResponseItems[SkillInDBModel]:
        """Getting all skills from the database

        Args:
            limit (int): Limit of skills received
            last_skill_key (str): The last skill key received in the previous request

        Returns:
            ResponseItems[SkillInDBModel]: Query result
        """
        return await self.__database_controller.get_skill_all(limit, last_skill_key)

    async def add_skill(self, skill_key: str, token: str) -> SkillInDBModel:
        """Add a skill to yourself

        Args:
            skill_key (str)
            token (str)

        Raises:
            HTTPException: If skill is not found, skill alreade exists or
            failed to add skill

        Returns:
            SkillInDBModel
        """
        user = await self.__user_controller.get_user_by_token(token)
        result = list(filter(lambda item: skill_key == item.key, user.skills))
        if len(result) > 0:
            raise HTTPException(status_code=400, detail="Skill already exists")

        skill = await self.__database_controller.get_skill_by_key(skill_key)
        if skill is None:
            raise HTTPException(status_code=404, detail="Skill not found")
        try:
            await self.__database_controller.append_skills_to_user(
                [skill.dict()], user.key
            )
            return skill
        except AppendSkillsException as e:
            raise HTTPException(status_code=400, detail=f"{e}")

    async def remove_skill(self, skill_key: str, token: str) -> List[SkillInDBModel]:
        """Delete a skill from yourself

        Args:
            skill_key (str)
            token (str)

        Raises:
            HTTPException: If skill is not found or failed to add skill

        Returns:
            List[SkillInDBModel]
        """
        user = await self.__user_controller.get_user_by_token(token)
        result = list(filter(lambda item: skill_key == item.key, user.skills))
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Skill not found")
        user.skills.remove(result[0])
        try:
            await self.__database_controller.update_simple_data_to_user(
                {"skills": (user.dict())["skills"]}, user.key
            )
            return user.skills
        except UpdateUserDataException as e:

            raise HTTPException(status_code=400, detail=f"{e}")
