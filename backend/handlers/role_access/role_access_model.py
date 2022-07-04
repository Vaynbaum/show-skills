from typing import Union
from pydantic import BaseModel

from handlers.role_access.enums.address_enum import AddressEnum
from handlers.role_access.enums.owner_enum import OwnerEnum


class RoleAccessModel(BaseModel):
    name: str
    owner: Union[OwnerEnum, None]
    addressee: Union[AddressEnum, None]

    def __identity_owner(self, user, key):
        if self.owner == OwnerEnum.ANY:
            return True
        if (self.owner == OwnerEnum.OWN) and user.key == key:
            return True
        return False

    def __allow_address(self, user):
        pass

    def check_owner_access(self, user, key: Union[str, None]):
        if self.owner is not None:
            if not self.__identity_owner(user, key):
                return False
        return True
