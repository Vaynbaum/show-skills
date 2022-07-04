import os
from typing import Union
from deta import Deta
from dotenv import load_dotenv

from db.abstract_database_handler import AbstractDatabaseHandler
from db.handlers.role_database_handler import RoleDatabaseHandler
from db.handlers.skill_database_handler import SkillDatabaseHandler
from db.handlers.user_database_handler import UserDatabaseHandler
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
