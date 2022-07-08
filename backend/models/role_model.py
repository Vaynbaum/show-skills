from typing import Union
from pydantic import BaseModel


class RoleModelResponse(BaseModel):
    name_ru: str
    name_en: str
    name_icon: Union[str, None]


class RoleModelInDB(RoleModelResponse):
    can_assign: bool
    key: Union[str, None]
