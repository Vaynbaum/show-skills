from abc import ABC, abstractmethod
from deta.base import FetchResponse

from db.models.role_model import RoleModel
from db.models.user_model import UserModelInDB, UserResponseModel


class AbstractDatabaseHandler(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> UserModelInDB | None:
        '''Получение одного пользователя по email из базы данных'''
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> UserResponseModel | None:
        '''Получение одного пользователя по username из базы данных'''
        pass
    
    @abstractmethod
    def get_user_all(self):
        '''Получение всех пользователей'''
        pass

    @abstractmethod
    def create_user(self, user: UserModelInDB) -> UserModelInDB | None:
        '''Добавление пользователя в базу данных'''
        pass

    @abstractmethod
    def get_user_by_key(self, key: str) -> UserModelInDB | None:
        '''Получение пользователя по ключу из базы данных'''
        pass

    @abstractmethod
    def delete_user_by_key(self, key: str) -> None:
        '''Удаление пользователя из базы данных по ключу'''
        pass

    @abstractmethod
    def get_role_by_name_en(self, title: str) -> RoleModel | None:
        '''Получение одной роли по названию на английском из базы данных'''
        pass

    @abstractmethod
    def get_role_by_key(self, key: str) -> RoleModel | None:
        '''Получение роли по ключу из базы данных'''
        pass
