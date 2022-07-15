from typing import Union
from handlers.access.owner.owner import Owner
from models.user_model import UserInDBModel


class OwnOwner(Owner):
    def check(
        self, user_initiator: UserInDBModel, user_creator: Union[UserInDBModel, None]
    ) -> bool:
        if user_creator is None:
            return False
        return user_initiator.key == user_creator.key
