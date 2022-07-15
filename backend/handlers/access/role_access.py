from typing import Union
from handlers.access.assign.assign import Assign
from handlers.access.owner.owner import Owner
from models.user_model import UserInDBModel


class RoleAccess:
    def __init__(self, name, owners: list[Owner] = [], assigns: list[Assign] = []):
        self.__name = name
        self.__owners = owners
        self.__assigns = assigns

    @property
    def name(self):
        return self.__name

    def check_to_user(self, user: UserInDBModel) -> bool:
        """Checking the possibility of assignment

        Args:
            user (UserInDBModel): user model

        Returns:
            bool: True if allowed and False otherwise
        """
        if len(self.__assigns) == 0:
            return True

        for assign in self.__assigns:
            if assign.check(user):
                return True

        return False

    def check_owner_access(
        self, user_initiator: UserInDBModel, user_creator: Union[UserInDBModel, None]
    ) -> bool:
        """Checks whether the initiator of the action on the creator's object is possible

        Args:
            user_initiator (UserInDBModel): user model initiator
            user_creator (Union[UserInDBModel, None]): user model creator

        Returns:
            bool: True if allowed and False otherwise
        """
        if len(self.__owners) == 0:
            return True

        for owner in self.__owners:
            if owner.check(user_initiator, user_creator):
                return True

        return False
