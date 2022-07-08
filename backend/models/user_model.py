from typing import List, Union
from pydantic import BaseModel

from models.link_model import LinkModel
from models.role_model import RoleModelResponse
from models.short_user_model_response import ShortUserModelResponse
from models.skill_model import SkillModelInDB
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


class UserModelInDB(BaseModel):
    username: str
    firstname: str
    lastname: str
    key: Union[str, None]
    url_photo: Union[str, None]

    place_residence: Union[str, None]
    email: str
    age: Union[int, None]
    followers: List[ShortUserModelResponse]
    links: List[LinkModel]
    role: Union[RoleModelResponse, None]
    skills: List[SkillModelInDB]

    subscriptions: List[SubscriptionModel]
    role_key: Union[str, None]
    password: str


class UserModelResponse(ShortUserModelResponse):
    place_residence: Union[str, None]
    email: str
    age: Union[int, None]
    followers: List[ShortUserModelResponse]
    links: List[LinkModel]
    role: Union[RoleModelResponse, None]
    skills: List[SkillModelInDB]


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
