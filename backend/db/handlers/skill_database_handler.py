from typing import Union
from deta import Deta

from models.skill_model import SkillModelInDB


class SkillDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__skills_db = deta.AsyncBase("skills")

    async def create(self, skill: SkillModelInDB) -> Union[SkillModelInDB, None]:
        """Добавление навыка в базу данных"""
        return await self.__skills_db.put(skill.dict())

    async def get_all(self, limit, last_user_key):
        """Получение всех навыков из базы данных"""
        return await self.__skills_db.fetch(limit=limit, last=last_user_key)

    # def get_role_by_name_en(self, title: str) -> RoleModelInDB | None:
    #     '''Получение одной роли по названию на английском из базы данных'''
    #     res_fetch = self.__roles_db.fetch({"name_en": title}, limit = 1)
    #     return res_fetch.items[0] if res_fetch.count > 0 else None

    # def get_role_by_key(self, key: str) -> RoleModelInDB | None:
    #     '''Получение роли по ключу из базы данных'''
    #     return self.__roles_db.get(key)
