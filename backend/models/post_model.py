from typing import List
from pydantic import BaseModel

from models.comment_model import CommentModel
from models.like_model import LikeModel
from models.skill_model import SkillInDBModel
from models.short_user_model_response import ShortUserModelResponse


class PostInputModel(BaseModel):
    name: str
    url_content: str
    skill: SkillInDBModel

    class Config:
        schema_extra = {
            "example": {
                "name": "UML диаграммы",
                "url_content": "http://localhost:8000/post/content/post_uml_zgqeuipptbrjwhd.html",
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
