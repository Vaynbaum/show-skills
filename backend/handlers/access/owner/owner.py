from abc import ABC, abstractmethod
from typing import Union

from models.user_model import UserInDBModel


class Owner(ABC):
    @abstractmethod
    def check(
        self, user_initiator: UserInDBModel, user_creator: Union[UserInDBModel, None]
    ) -> bool:
        """Checks whether the initiator of the action on the creator's object is possible

        Args:
            user_initiator (UserInDBModel): user model initiator
            user_creator (Union[UserInDBModel, None]): user model creator

        Returns:
            bool: True if allowed and False otherwise
        """
        pass
