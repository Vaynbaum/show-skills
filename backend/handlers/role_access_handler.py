from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from pyparsing import Enum

from db.abstract_database_handler import AbstractDatabaseHandler
from db.models.user_model import UserModelInDB
from handlers.jwt_handler import JWTHandler


class OwnerEnum(Enum):
    OWN = 0
    ANY = 1


class AddressEnum(Enum):
    ANY = 0
    USER = 1
    ADMIN = 2
    SUPER_ADMIN = 3


class RoleModel(BaseModel):
    name: str
    owner: OwnerEnum | None
    addressee: AddressEnum | None

    def __identity_owner(self, user, key):
        if self.owner == OwnerEnum.ANY:
            return True
        if (self.owner == OwnerEnum.OWN) and user['key'] == key:
            return True
        return False

    def __allow_address(self, user):
        pass

    def check_access(self, user, key: str | None):
        if self.owner is not None:
            if not self.__identity_owner(user, key):
                return False
        if self.addressee is not None:
            pass
        return True


class AccessHandler:
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__database_controller = database_controller
        self.__jwt_handler = JWTHandler()

    def __get_user_by_token(self, token):
        '''Получение пользователя из бд по ключу из токена'''
        sub = self.__jwt_handler.decode_token(token)
        return self.__database_controller.get_user_by_key(sub)

    def __find_access_role(self, roles: list[RoleModel], user: UserModelInDB | None):
        '''Проверка существования пользователя и его возможность доступа'''
        if user is not None:
            for role in roles:
                if role['name'] == user['role']['name_en']:
                    return RoleModel(**role)
        return None

    def maker_role_access(self, roles: list[RoleModel],
                          credentials: HTTPAuthorizationCredentials,
                          key_author: str | None = None):
        '''Создание декоратора доступа пользователя по роли'''
        def decorator(func):
            '''Декоратор'''
            def wrapped(*args, **kwargs):
                '''Обёртка'''
                user = self.__get_user_by_token(credentials.credentials)
                # Если роль пользователя имеет доступ к функции
                role = self.__find_access_role(roles, user)
                if (role is not None) and role.check_access(user, key_author):
                    return func(*args, **kwargs)
                else:
                    return {"message": "No access"}
            return wrapped
        return decorator
