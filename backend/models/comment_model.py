from typing import Union
from pydantic import BaseModel

from models.short_user_model_response import ShortUserModelResponse


class CommentInputModel(BaseModel):
    text: str
    name: str


class CommentModel(CommentInputModel):
    author: ShortUserModelResponse
    key: Union[str, None]
    date_create: int
