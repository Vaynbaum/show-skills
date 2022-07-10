from typing import Union
from pydantic import BaseModel
from handlers.datetime_handler import DatetimeHandler

from models.short_user_model_response import ShortUserModelResponse
from consts.name_format_event import ONLINE

datetime_handler = DatetimeHandler()


class EventInputModel(BaseModel):
    name: str
    date: int
    format_event: Union[str, dict]
    place: dict

    class Config:
        schema_extra = {
            "example": {
                "name": "Вебинар по Angular",
                "date": datetime_handler.now_next_days(2),
                "format_event": ONLINE,
                "place": {"name_platform": "VK", "URL": "https://example"},
            }
        }


class EventInDBModel(EventInputModel):
    key: Union[str, None]
    author: ShortUserModelResponse
