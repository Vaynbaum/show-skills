from pydantic import BaseModel

from consts.name_attribute_access_roles import NAME_ATTR_OWNER
from consts.owner_enum import OwnerEnum


class RoleAccessModel(BaseModel):
    name: str
    attributes: dict = None

    def __identity_owner(self, user, key):
        owner = self.attributes[NAME_ATTR_OWNER]
        if owner == OwnerEnum.ANY:
            return True
        if (owner == OwnerEnum.OWN) and user.key == key:
            return True
        return False

    def __allow_address(self, user):
        pass

    def check_owner_access(self, user, key: str = None):
        if NAME_ATTR_OWNER is self.attributes:
            if not self.__identity_owner(user, key):
                return False
        return True
