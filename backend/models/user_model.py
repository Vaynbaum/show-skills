from typing import List, Union
from pydantic import BaseModel

from models.link_model import LinkModel
from models.role_model import RoleDataModel
from models.short_response_user_model import ShortResponseUserModel
from models.subscription_model import SubscriptionModel


class AuthModel(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ivanov@mail.ru",
                "password": "secret",
            }
        }


class SignupModel(BaseModel):
    email: str
    username: str
    password: str
    lastname: str
    firstname: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ivanov@mail.ru",
                "username": "ivanov",
                "password": "secret",
                "lastname": "Иванов",
                "firstname": "Иван",
            }
        }


class UserUpdateModel(BaseModel):
    email: str
    username: str
    lastname: str
    firstname: str


class UserModelInDB(BaseModel):
    email: str
    username: str
    password: str
    lastname: str
    firstname: str
    role: Union[RoleDataModel, None]
    role_key: Union[str, None]
    key: Union[str, None]
    age: Union[int, None]
    url_photo: Union[str, None]
    place_residence: Union[str, None]
    followers: List[ShortResponseUserModel]
    subscriptions: List[SubscriptionModel]
    links: List[LinkModel]


class ResponseUserModel(ShortResponseUserModel):
    email: str
    role: Union[RoleDataModel, None]
    age: Union[int, None]
    place_residence: Union[str, None]


class UserUpdateDataModel(BaseModel):
    password: str
    lastname: str
    firstname: str
    age: Union[int, None]
    place_residence: Union[str, None]

    class Config:
        schema_extra = {
            "example": {
                "password": "secret",
                "lastname": "Иванов",
                "firstname": "Иван",
                "age": 20,
                "place_residence": "Нижний Новгород",
            }
        }
