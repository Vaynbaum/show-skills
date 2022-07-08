from typing import Union
from pydantic import BaseModel
from datetime import datetime

from models.short_user_model_response import ShortUserModelResponse


class CommentModel(BaseModel):
    key: Union[str, None]
    text: str
    date_create: datetime
    name: str
    user_key: str
    post_key: str
    author: ShortUserModelResponse
