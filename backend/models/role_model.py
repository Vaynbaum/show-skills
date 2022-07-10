from typing import Union
from pydantic import BaseModel


class RoleModelResponse(BaseModel):
    name_ru: str
    name_en: str
    url: Union[str, None]


class RoleInDBModel(RoleModelResponse):
    can_assign: bool
    key: Union[str, None]
