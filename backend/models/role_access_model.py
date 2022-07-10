from pydantic import BaseModel

from consts.name_attribute_access_roles import NAME_ATTR_OWNER, NAME_ATTR_TO_ASSIGN
from consts.owner_enum import OwnerEnum
from models.user_model import UserInDBModel


class RoleAccessModel(BaseModel):
    name: str
    attributes: dict = None

    def check_to_user(self, user: UserInDBModel) -> bool:
        """Checking the possibility of assignment

        Args:
            user (UserInDBModel): user model

        Returns:
            bool: True if allowed and False otherwise
        """
        if NAME_ATTR_TO_ASSIGN in self.attributes:
            allow_roles = self.attributes[NAME_ATTR_TO_ASSIGN]
            if user.role.name_en in allow_roles:
                return True
            else:
                return False
        else:
            return True

    def check_owner_access(self, user: UserInDBModel, key: str = None) -> bool:
        """Checking the possibility of an action on an object

        Args:
            user (UserInDBModel): user model
            key (str, optional): user's key. Defaults to None.

        Returns:
            bool: True if allowed and False otherwise
        """
        if NAME_ATTR_OWNER in self.attributes:
            owner = self.attributes[NAME_ATTR_OWNER]
            if owner == OwnerEnum.ANY:
                return True
            if (owner == OwnerEnum.OWN) and user.key == key:
                return True
            return False
        else:
            return True
