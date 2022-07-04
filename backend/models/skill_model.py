from typing import Union
from pydantic import BaseModel


class SkillModelInDB(BaseModel):
    key: Union[str, None]
    name: str
    scope: str
    name_icon: Union[str, None]


class SkillCreateDataModel(BaseModel):
    name: str
    scope: str
    name_icon: Union[str, None]

    class Config:
        schema_extra = {
            "example": {
                "name": "Python",
                "scope": "Программирование",
                "name_icon": "python.png",
            }
        }
