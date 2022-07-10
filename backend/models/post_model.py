from typing import List
from pydantic import BaseModel

from models.comment_model import CommentModel
from models.like_model import LikeModel
from models.skill_model import SkillInDBModel
from models.short_user_model_response import ShortUserModelResponse


class PostInputModel(BaseModel):
    name: str
    content_html: str
    skill: SkillInDBModel


class PostInDBModel(PostInputModel):
    date_create: int
    author: ShortUserModelResponse
    author_key: str
    likes: List[LikeModel]
    comments: List[CommentModel]
    key: str = None