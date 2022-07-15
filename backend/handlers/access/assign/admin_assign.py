from consts.name_roles import ADMIN
from handlers.access.assign.assign import Assign
from models.user_model import UserInDBModel


class AdminAssign(Assign):
    def __init__(
        self,
    ):
        self.__name = ADMIN

    def check(self, user: UserInDBModel) -> bool:
        return self.__name == user.role.name_en
