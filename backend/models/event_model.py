from calendar import timegm
from datetime import datetime
from typing import Union
from pydantic import BaseModel

from models.short_user_model_response import ShortUserModelResponse
from consts.name_format_event import ONLINE


class EventModelInput(BaseModel):
    name: str
    date: int
    format_event: Union[str, dict]
    place: dict

    class Config:
        schema_extra = {
            "example": {
                "name": "Вебинар по Angular",
                "date": timegm((datetime(2022, 7, 10, 11)).timetuple()),
                "format_event": ONLINE,
                "place": {"name_platform": "VK", "URL": "https://example"},
            }
        }


class EventModelInDB(EventModelInput):
    key: Union[str, None]
    author: ShortUserModelResponse
