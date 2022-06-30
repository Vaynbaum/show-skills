from datetime import datetime
from typing import List, TypeVar
from pydantic import BaseModel

from db.models.attachments_model import AttachmentModel
from db.models.comment_model import CommentModel
from db.models.like_model import LikeModel
from db.models.skill_model import SkillModel
from db.models.user_model import UserResponseModel


class PostModel(BaseModel):
    key: str | None
    name: str
    date: datetime
    text: str
    # type_object: int
    author: UserResponseModel
    author_key: str
    skills: List[TypeVar('SkillModel', bound=SkillModel)]
    attachments: List[TypeVar('AttachmentModel', bound=AttachmentModel)]
    likes: List[TypeVar('LikeModel', bound=LikeModel)]
    comments: List[TypeVar('CommentModel', bound=CommentModel)]
