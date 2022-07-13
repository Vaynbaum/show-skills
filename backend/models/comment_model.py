from typing import Union
from pydantic import BaseModel

from models.short_user_model_response import ShortUserModelResponse


class CommentInputModel(BaseModel):
    text: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Автор прекрасно объяснил данный материал",
                "name": "Прекрасная статья",
            }
        }


class CommentModel(CommentInputModel):
    author: ShortUserModelResponse
    key: Union[str, None]
    date_create: int
