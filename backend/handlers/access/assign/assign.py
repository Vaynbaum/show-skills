from abc import ABC, abstractmethod

from models.user_model import UserInDBModel


class Assign(ABC):
    @abstractmethod
    def check(self, user: UserInDBModel) -> bool:
        """Checks the possibility of assignment

        Args:
            user (UserInDBModel): user's model

        Returns:
            bool: True if it is possible to assign and False otherwise
        """        
        pass
