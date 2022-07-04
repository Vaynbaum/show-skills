from typing import List, Union
from pydantic import BaseModel

from models.role_model import RoleDataModel


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
    password: str
    lastname: str
    firstname: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ivanov@mail.ru",
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


class ShortResponseUserModel(BaseModel):
    username: str
    lastname: str
    key: Union[str, None]
    firstname: str
    url_photo: Union[str, None]


class SubscriptionModel(BaseModel):
    favorite: ("ShortResponseUserModel")
    number_visits: int = 1


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
    followers: List[("ShortResponseUserModel")]
    subscriptions: List[("SubscriptionModel")]

    @staticmethod
    def get_username_by_email(email: str) -> str:
        email_splitted: str = email.split("@")
        return email_splitted[0] if len(email_splitted) > 1 else email


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
