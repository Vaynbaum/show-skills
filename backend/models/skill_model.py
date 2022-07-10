from typing import Union
from pydantic import BaseModel


class SkillInDBModel(BaseModel):
    key: Union[str, None]
    name: str
    scope: str
    url: Union[str, None]


class SkillCreateDataModel(BaseModel):
    name: str
    scope: str
    url: Union[str, None]

    class Config:
        schema_extra = {
            "example": {
                "name": "Python",
                "scope": "Программирование",
                "url": "python.png",
            }
        }
