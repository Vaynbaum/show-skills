from abc import ABC, abstractmethod
from db.models.user_model import AbstractUserModelInDB


class AbstractDetaDatabaseHandler(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str):
        pass

    @abstractmethod
    def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    def create_user(self, user: AbstractUserModelInDB):
        pass
