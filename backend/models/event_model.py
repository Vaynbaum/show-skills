from typing import Union
from pydantic import BaseModel
from datetime import datetime, timedelta


from models.short_user_model_response import ShortUserModelResponse
from consts.name_format_event import ONLINE


class EventInputModel(BaseModel):
    name: str
    date: int
    format_event: str
    place: dict

    class Config:
        schema_extra = {
            "example": {
                "name": "Вебинар по Angular",
                "date": datetime.now() + timedelta(2),
                "format_event": ONLINE,
                "place": {"name_platform": "VK", "URL": "https://example"},
            }
        }


class EventInDBModel(EventInputModel):
    key: Union[str, None]
    author: ShortUserModelResponse
    date: int
