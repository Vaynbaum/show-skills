from pydantic import BaseModel

from models.short_response_user_model import ShortResponseUserModel


class SubscriptionModel(BaseModel):
    favorite: ShortResponseUserModel
    number_visits: int = 1
