from pydantic import BaseModel
from datetime import datetime

from db.models.user_model import UserResponseModel


class CommentModel(BaseModel):
    key: str | None
    # type_object: int
    text: str
    date_create: datetime
    name: str
    user_key: str
    post_key: str
    author: UserResponseModel
