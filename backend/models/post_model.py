from datetime import datetime
from typing import List, Union
from pydantic import BaseModel

from models.comment_model import CommentModel
from models.like_model import LikeModel
from models.skill_model import SkillInDBModel
from models.short_user_model_response import ShortUserModelResponse


class PostInputModel(BaseModel):
    name: str
    content_html: str
    skill: SkillInDBModel

    class Config:
        schema_extra = {
            "example": {
                "name": "UML диаграммы",
                "content_html": "<p>уц ац цуау цуа уц wef e<img alt='' src='http://localhost:8000/post/photo/qxyzxrtz_%D0%91%D0%B0%D0%B7%D0%B0%D0%94%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.png' style='width:567px' /></p>",
                "skill": {
                    "key": "3ed34r43f3",
                    "name": "UML-диаграммы",
                    "scope": "Программирование",
                    "url": "http://localhost:8000/skill/icon/uml.png",
                },
            }
        }


class PostInDBModel(PostInputModel):
    date_create: int
    author: ShortUserModelResponse
    likes: List[LikeModel]
    comments: List[CommentModel]
    key: str = None
