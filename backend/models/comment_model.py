from typing import Union
from pydantic import BaseModel
from datetime import datetime

from models.user_model import ResponseUserModel


class CommentModel(BaseModel):
    key: Union[str, None]
    # type_object: int
    text: str
    date_create: datetime
    name: str
    user_key: str
    post_key: str
    author: ResponseUserModel
