from pyparsing import Enum


class AddressEnum(Enum):
    ANY = 0
    USER = 1
    ADMIN = 2
    SUPER_ADMIN = 3
    OWN = 4
