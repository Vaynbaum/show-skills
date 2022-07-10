from pydantic import BaseModel

from models.short_user_model_response import ShortUserModelResponse


class LikeModel(BaseModel):
    user: ShortUserModelResponse
