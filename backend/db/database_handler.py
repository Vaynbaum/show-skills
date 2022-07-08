import os
from typing import Union
from deta import Deta
from dotenv import load_dotenv

from db.abstract_database_handler import AbstractDatabaseHandler
from db.handlers.event_database_handler import EventDatabaseHandler
from db.handlers.role_database_handler import RoleDatabaseHandler
from db.handlers.skill_database_handler import SkillDatabaseHandler
from db.handlers.user_database_handler import UserDatabaseHandler
from exceptions.append_links_exception import AppendLinksException
from exceptions.append_skills_exception import AppendSkillsException
from exceptions.update_event_exception import UpdateEventException
from exceptions.update_item_exception import UpdateItemException
from exceptions.update_user_data_exception import UpdateUserDataException
from models.event_model import EventModelInDB, EventModelInput
from models.response_items import ResponseItems
from models.role_model import RoleModelInDB
from models.skill_model import SkillCreateDataModel, SkillModelInDB
from models.user_model import UserModelInDB, UserModelResponse


class DatabaseHandler(AbstractDatabaseHandler):
    def __init__(self):
        load_dotenv()
        self.__deta = Deta(os.getenv("DETA_PROJECT_KEY"))
        self.__user_handler = UserDatabaseHandler(self.__deta)
        self.__role_handler = RoleDatabaseHandler(self.__deta)
        self.__skill_handler = SkillDatabaseHandler(self.__deta)
        self.__event_handler = EventDatabaseHandler(self.__deta)

    # User
    async def get_user_by_email(self, email: str) -> Union[UserModelInDB, None]:
        return await self.__user_handler.get_one_by_query({"email": email})

    async def get_user_by_username(self, username: str) -> Union[UserModelInDB, None]:
        return await self.__user_handler.get_one_by_query({"username": username})

    async def get_user_by_key(self, key: str) -> Union[UserModelInDB, None]:
        return await self.__user_handler.get_by_key(key)

    async def get_user_all(
        self, limit: int = 1000, last_user_key: str = None
    ) -> ResponseItems[UserModelResponse]:
        return await self.__user_handler.get_many_by_query(
            limit=limit, last_user_key=last_user_key
        )

    async def put_many_users(self, users: list) -> dict:
        return await self.__user_handler.put_many(users)

    async def create_user(self, data: UserModelInDB) -> Union[UserModelInDB, None]:
        return await self.__user_handler.create(data)

    async def delete_user_by_key(self, key: str) -> None:
        return await self.__user_handler.delete_by_key(key)

    async def append_links_to_user(self, links: list, key: str) -> None:
        try:
            return await self.__user_handler.append_links(links, key)
        except UpdateItemException as e:
            print(e)
            raise AppendLinksException("Adding links to the user is not successful")

    async def append_skills_to_user(self, skills: list, key: str) -> None:
        try:
            return await self.__user_handler.append_skills(skills, key)
        except UpdateItemException as e:
            print(e)
            raise AppendSkillsException("Adding skills to the user is not successful")

    async def simple_data_update_to_user(self, data: dict, key: str) -> None:
        try:
            return await self.__user_handler.simple_data_update(data, key)
        except UpdateItemException as e:
            print(e)
            raise UpdateUserDataException("Updating user data was not successful")

    # Role
    async def get_role_by_name_en(self, name: str) -> Union[RoleModelInDB, None]:
        return await self.__role_handler.get_one_by_query({"name_en": name})

    async def get_role_by_key(self, key: str) -> Union[RoleModelInDB, None]:
        return await self.__role_handler.get_by_key(key)

    async def get_role_all_can_assign(
        self, limit: int = 1000, last_role_key: str = None
    ) -> ResponseItems[RoleModelInDB]:
        return await self.__role_handler.get_many_by_query(
            {"can_assign": True}, limit, last_role_key
        )

    # Skill
    async def create_skill(
        self, data: SkillCreateDataModel
    ) -> Union[SkillModelInDB, None]:
        return await self.__skill_handler.create(data)

    async def get_skill_all(
        self, limit: int = 1000, last_skill_key: str = None
    ) -> ResponseItems[SkillModelInDB]:
        return await self.__skill_handler.get_many_by_query(
            limit=limit, last_skill_key=last_skill_key
        )

    async def get_skill_by_key(self, key: str) -> Union[SkillModelInDB, None]:
        return await self.__skill_handler.get_by_key(key)

    # Event
    async def create_event(self, event: EventModelInDB) -> Union[EventModelInDB, None]:
        return await self.__event_handler.create(event)

    async def get_events_by_query(
        self, query: dict = None, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventModelInDB]:
        return await self.__event_handler.get_many_by_query(
            query, limit, last_event_key
        )

    async def get_all_events(
        self, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventModelInDB]:
        return await self.__event_handler.get_many_by_query(
            limit=limit, last_event_key=last_event_key
        )

    async def delete_event_by_key(self, key: str) -> None:
        return await self.__event_handler.delete(key)

    async def get_event_by_key(self, key: str) -> Union[EventModelInDB, None]:
        return await self.__event_handler.get_by_key(key)

    async def update_event_by_key(self, event: EventModelInput, key: str) -> None:
        try:
            return await self.__event_handler.update(event, key)
        except UpdateItemException as e:
            print(e)
            raise UpdateEventException("Updating event data was not successful")
