from typing import Union
from deta import Deta

from models.response_items import ResponseItems
from models.skill_model import SkillCreateDataModel, SkillInDBModel


class SkillDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__skills_db = deta.AsyncBase("skills")

    async def create(self, skill: SkillCreateDataModel) -> Union[SkillInDBModel, None]:
        """Adding a new skill to the database

        Args:
            skill (SkillCreateDataModel): New skill model

        Returns:
            Union[SkillInDBModel, None]: The model of the skill added to the database otherwise None
        """
        try:
            skill = await self.__skills_db.put(skill.dict())
            return SkillInDBModel(**skill)
        except:
            return None

    async def get_many_by_query(
        self, query: dict = None, limit: int = 1000, last_skill_key: str = None
    ) -> ResponseItems[SkillInDBModel]:
        """Get skills by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.
            limit (int, optional): Limit of skills received. Defaults to 1000.
            last_skill_key (str, optional): The last skill key received in the previous request.
            Defaults to None.

        Returns:
            ResponseItems[SkillInDBModel]: Query result
        """
        result = await self.__skills_db.fetch(query, limit=limit, last=last_skill_key)
        return ResponseItems[SkillInDBModel](
            count=result.count, last=result.last, items=result.items
        )

    async def get_by_key(self, key: str) -> Union[SkillInDBModel, None]:
        """Get a skill by key from the database

        Args:
            key (str): The skill key in the database

        Returns:
            Union[SkillInDBModel, None]: If a skill is found, then returns SkillInDBModel otherwise None
        """
        skill = await self.__skills_db.get(key)
        return SkillInDBModel(**skill) if skill is not None else None
