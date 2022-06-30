from pydantic import BaseModel


class SkillModel(BaseModel):
    key: str | None
    name: str
    description: str
    # type_object: str
    # type_object_key: str
    url_icon: str | None
