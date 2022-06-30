from pydantic import BaseModel

from db.models.role_model import RoleDataModel


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


class UserModelInDB(BaseModel):
    email: str
    username: str
    password: str
    lastname: str
    firstname: str
    role: RoleDataModel
    role_key: str
    key: str | None
    age: int | None
    url_photo: str | None
    place_residence: str | None

    @staticmethod
    def get_username_by_email(email: str) -> str:
        email_splitted: str = email.split("@")
        return email_splitted[0] if len(email_splitted) > 1 else email


class UserResponseModel(BaseModel):
    email: str
    username: str
    lastname: str
    firstname: str
    role: RoleDataModel
    key: str | None
    age: int | None
    url_photo: str | None
    place_residence: str | None
