from pyparsing import Enum


class AddressEnum(Enum):
    ANY = 0
    OWN = 1
    USER = 2
    ADMIN = 3
    SUPER_ADMIN = 4
