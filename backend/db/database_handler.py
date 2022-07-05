import os
from typing import Union
from deta import Deta
from dotenv import load_dotenv
from fastapi import HTTPException

from db.abstract_database_handler import AbstractDatabaseHandler
from db.handlers.event_database_handler import EventDatabaseHandler
from db.handlers.role_database_handler import RoleDatabaseHandler
from db.handlers.skill_database_handler import SkillDatabaseHandler
from db.handlers.user_database_handler import UserDatabaseHandler
from models.event_model import EventModelInDB, EventModelInput
from models.items import ResponseItems
from models.role_model import RoleModelInDB
from models.skill_model import SkillCreateDataModel, SkillModelInDB
from models.user_model import UserModelInDB, ResponseUserModel


class DatabaseHandler(AbstractDatabaseHandler):
    def __init__(self):
        load_dotenv()
        self.__deta = Deta(os.getenv("DETA_PROJECT_KEY"))
        self.__user_handler = UserDatabaseHandler(self.__deta)
        self.__role_handler = RoleDatabaseHandler(self.__deta)
        self.__skill_handler = SkillDatabaseHandler(self.__deta)
        self.__event_handler = EventDatabaseHandler(self.__deta)

    async def get_user_by_email(self, email: str):
        user = await self.__user_handler.get_by_field(email, "email")
        return UserModelInDB(**user) if user is not None else None

    async def get_user_by_username(self, username: str):
        user = await self.__user_handler.get_by_field(username, "username")
        return UserModelInDB(**user) if user is not None else None

    async def get_user_by_key(self, key: str):
        user = await self.__user_handler.get_by_key(key)
        return UserModelInDB(**user) if user is not None else None

    async def get_user_all(self, limit, last_user_key):
        result = await self.__user_handler.get_all(limit, last_user_key)
        return ResponseItems[ResponseUserModel](
            count=result.count, last=result.last, items=result.items
        )

    # async def get_user_by_complex_query(self, query, limit, last_user_key):
    #     result = await self.__user_handler.get_by_query(query, limit, last_user_key)
    #     # return ResponseItems[ResponseUserModel](
    #     #     count=result.count, last=result.last, items=result.items
    #     # )
    #     return None

    async def put_many_users(self, users: list):
        result = await self.__user_handler.put_many(users)
        return result

    async def create_user(self, data: UserModelInDB):
        user = await self.__user_handler.create(data)
        return UserModelInDB(**user) if user is not None else None

    async def delete_user_by_key(self, key: str):
        await self.__user_handler.delete_by_key(key)
        return None

    async def append_links_to_user(self, links: list, key: str) -> None:
        return await self.__user_handler.append_links(links, key)

    async def update_simple_data_to_user(self, data: dict, key: str) -> None:
        return await self.__user_handler.update_simple_data(data, key)

    async def get_role_by_name_en(self, title: str):
        role = await self.__role_handler.get_by_name_en(title)
        return RoleModelInDB(**role) if role is not None else None

    async def get_role_by_key(self, key: str):
        role = await self.__role_handler.get_by_key(key)
        return RoleModelInDB(**role) if role is not None else None

    async def create_skill(
        self, data: SkillCreateDataModel
    ) -> Union[SkillModelInDB, None]:
        skill = await self.__skill_handler.create(data)
        return SkillModelInDB(**skill) if skill is not None else None

    async def get_skill_all(
        self, limit, last_user_key
    ) -> ResponseItems[SkillModelInDB]:
        result = await self.__skill_handler.get_all(limit, last_user_key)
        return ResponseItems[SkillModelInDB](
            count=result.count, last=result.last, items=result.items
        )

    async def create_event(self, event: EventModelInDB):
        return await self.__event_handler.create(event)

    async def get_event_by_query(self, query):
        result = await self.__event_handler.get_by_query(query)
        return ResponseItems[EventModelInDB](
            count=result.count, last=result.last, items=result.items
        )

    async def get_all_events(self):
        result = await self.__event_handler.get_by_query({})
        return ResponseItems[EventModelInDB](
            count=result.count, last=result.last, items=result.items
        )

    async def delete_event_by_key(self, key: str) -> None:
        """Удаление пользователя из базы данных по ключу"""
        return await self.__event_handler.delete(key)

    async def get_event_by_key(self, key: str):
        event = await self.__event_handler.get_by_key(key)
        return EventModelInDB(**event) if event is not None else None

    async def update_event_by_key(self, event: EventModelInput, key: str):
        return await self.__event_handler.update(event, key)
