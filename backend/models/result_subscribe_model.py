from pydantic import BaseModel

from models.user_model import UserModelResponse


class ResultSubscriptionModel(BaseModel):
    favorite: UserModelResponse
    follower: UserModelResponse
