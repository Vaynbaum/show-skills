from datetime import datetime
from typing import List, TypeVar, Union
from pydantic import BaseModel

from models.attachments_model import AttachmentModel
from models.comment_model import CommentModel
from models.like_model import LikeModel
from models.skill_model import SkillModelInDB
from models.short_response_user_model import ShortResponseUserModel


class PostModel(BaseModel):
    key: Union[str, None]
    name: str
    date: datetime
    text: str
    author: ShortResponseUserModel
    author_key: str
    skills: List[TypeVar("SkillModelInDB", bound=SkillModelInDB)]
    attachments: List[TypeVar("AttachmentModel", bound=AttachmentModel)]
    likes: List[TypeVar("LikeModel", bound=LikeModel)]
    comments: List[TypeVar("CommentModel", bound=CommentModel)]
