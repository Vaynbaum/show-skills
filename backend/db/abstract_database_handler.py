from abc import ABC, abstractmethod
from typing import Union
from models.items import ResponseItems

from models.role_model import RoleModelInDB
from models.skill_model import SkillModelInDB
from models.user_model import UserModelInDB, ResponseUserModel


class AbstractDatabaseHandler(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Union[UserModelInDB, None]:
        """Получение одного пользователя по email из базы данных"""
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Union[UserModelInDB, None]:
        """Получение одного пользователя по username из базы данных"""
        pass

    @abstractmethod
    async def get_user_all(
        self, limit, last_user_key
    ) -> ResponseItems[ResponseUserModel]:
        """Получение всех пользователей"""
        pass

    # @abstractmethod
    # async def get_user_by_complex_query(
    #     self, query, limit, last_user_key
    # ) -> ResponseItems[UserModelInDB]:
    #     """Получение пользователей по сложному запросу"""
    #     pass

    @abstractmethod
    async def create_user(self, user: UserModelInDB) -> Union[UserModelInDB, None]:
        """Добавление пользователя в базу данных"""
        pass

    @abstractmethod
    async def get_user_by_key(self, key: str) -> Union[UserModelInDB, None]:
        """Получение пользователя по ключу из базы данных"""
        pass

    @abstractmethod
    async def put_many_users(self, users: list):
        """Добавление нескольких пользователей из базы данных"""
        pass

    @abstractmethod
    async def delete_user_by_key(self, key: str) -> None:
        """Удаление пользователя из базы данных по ключу"""
        pass

    @abstractmethod
    async def get_role_by_name_en(self, title: str) -> Union[RoleModelInDB, None]:
        """Получение одной роли по названию на английском из базы данных"""
        pass

    @abstractmethod
    async def get_role_by_key(self, key: str) -> Union[RoleModelInDB, None]:
        """Получение роли по ключу из базы данных"""
        pass

    @abstractmethod
    async def create_skill(self, skill: SkillModelInDB) -> Union[SkillModelInDB, None]:
        """Добавление навыка в базу данных"""
        pass

    @abstractmethod
    async def create_skill(self, skill: SkillModelInDB) -> Union[SkillModelInDB, None]:
        """Добавление навыка в базу данных"""
        pass

    @abstractmethod
    async def get_skill_all(
        self, limit, last_user_key
    ) -> ResponseItems[SkillModelInDB]:
        """Получение всех навыков"""
        pass
