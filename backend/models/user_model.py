from typing import List, Union
from pydantic import BaseModel
from datetime import datetime

from handlers.datetime_handler import DatetimeHandler
from models.link_model import LinkModel
from models.role_model import RoleModelResponse
from models.short_user_model_response import ShortUserModelResponse
from models.skill_model import SkillInDBModel
from models.subscription_model import SubscriptionModel

datetime_handler = DatetimeHandler()

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


class UserInDBModel(BaseModel):
    username: str
    firstname: str
    lastname: str
    key: Union[str, None]
    url: Union[str, None]

    place_residence: Union[str, None]
    email: str
    birth_date: Union[int, None]
    followers: List[ShortUserModelResponse]
    links: List[LinkModel]
    role: Union[RoleModelResponse, None]
    skills: List[SkillInDBModel]

    subscriptions: List[SubscriptionModel]
    role_key: Union[str, None]
    password: str


class UserModelResponse(ShortUserModelResponse):
    place_residence: Union[str, None]
    email: str
    birth_date: Union[int, None]
    followers: List[ShortUserModelResponse]
    links: List[LinkModel]
    role: Union[RoleModelResponse, None]
    skills: List[SkillInDBModel]


class UserAdditionalDataModel(BaseModel):
    birth_date: Union[int, None]
    place_residence: Union[str, None]

    class Config:
        schema_extra = {
            "example": {
                "birth_date": datetime_handler.convert_to_int(datetime(1999, 9, 24)),
                "place_residence": "Нижний Новгород",
            }
        }
