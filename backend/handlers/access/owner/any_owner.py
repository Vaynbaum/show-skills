from typing import Union
from handlers.access.owner.owner import Owner
from models.user_model import UserInDBModel


class AnyOwner(Owner):
    def check(
        self, user_initiator: UserInDBModel, user_creator: Union[UserInDBModel, None]
    ) -> bool:
        return True
