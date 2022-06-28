from pydantic import BaseModel


class AuthSchema(BaseModel):
    email: str
    password: str


class SignupSchema(BaseModel):
    email: str
    password: str
    lastname: str
    firstname: str


class UserSchemaInDB(BaseModel):
    email: str
    username: str
    password: str
    lastname: str
    firstname: str
    key: str = None
    age: int = None
    place_residence: str = None

    def get_username_by_email(email: str) -> str:
        email_splitted: str = email.split("@")
        return email_splitted[0] if len(email_splitted) > 1 else email


class UserResponse(BaseModel):
    email: str
    username: str
    lastname: str
    firstname: str
    age: int = None
    place_residence: str = None
