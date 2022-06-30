from enum import Enum


class Action(Enum):
    delete = 0
    update = 1
    create = 2
    get = 3
    assign = 4


class AtributeActionKey(Enum):
    own_key = 0
    any_key = 1


class AtributeActionAssignRole(Enum):
    user = 0
    admin = 1
    super_admin = 2
