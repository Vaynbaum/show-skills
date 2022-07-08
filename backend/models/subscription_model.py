from pydantic import BaseModel

from models.short_user_model_response import ShortUserModelResponse


class SubscriptionModel(BaseModel):
    favorite: ShortUserModelResponse
    number_visits: int = 1
