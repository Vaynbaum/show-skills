from pydantic import BaseModel

from models.short_user_model_response import ShortUserModelResponse


class SuggestionInputModel(BaseModel):
    title: str
    content: str


class SuggestionTickModel(BaseModel):
    completed: bool
    readed: bool


class SuggestionInDBModel(SuggestionInputModel, SuggestionTickModel):
    key: str = None
    sender: ShortUserModelResponse
