from abc import ABC, abstractmethod
from typing import Union
from models.event_model import EventModelInDB, EventModelInput
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
    async def append_links_to_user(self, links: list, key: str) -> None:
        """Добавление ссылок пользователя в базу данных"""
        pass

    @abstractmethod
    async def update_simple_data_to_user(self, data: dict, key: str) -> None:
        """Изменение данных пользователя в базе данных"""
        pass

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

    @abstractmethod
    async def create_event(self, event: EventModelInDB) -> EventModelInDB:
        pass

    @abstractmethod
    async def get_event_by_query(self, query) -> ResponseItems[EventModelInDB]:
        pass

    @abstractmethod
    async def get_all_events(self) -> ResponseItems[EventModelInDB]:
        pass

    @abstractmethod
    async def delete_event_by_key(self, key: str) -> None:
        """Удаление пользователя из базы данных по ключу"""
        pass

    @abstractmethod
    async def get_event_by_key(self, key: str) -> Union[EventModelInDB, None]:
        pass

    @abstractmethod
    async def update_event_by_key(self, event: EventModelInput, key: str) -> None:
        """Удаление пользователя из базы данных по ключу"""
        pass
