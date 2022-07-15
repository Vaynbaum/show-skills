from consts.name_roles import USER
from handlers.access.assign.assign import Assign
from models.user_model import UserInDBModel


class UserAssign(Assign):
    def __init__(
        self,
    ):
        self.__name = USER

    def check(self, user: UserInDBModel) -> bool:
        return self.__name == user.role.name_en
