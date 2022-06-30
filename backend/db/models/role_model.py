from pydantic import BaseModel


class RoleModel(BaseModel):
    key: str | None
    name_ru: str
    name_en: str
    url_icon: str | None

class RoleDataModel(BaseModel):
    name_ru: str
    name_en: str
    url_icon: str | None