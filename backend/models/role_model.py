from typing import Union
from pydantic import BaseModel


class RoleDataModel(BaseModel):
    name_ru: str
    name_en: str
    name_icon: Union[str, None]


class RoleModelInDB(RoleDataModel):
    key: Union[str, None]
