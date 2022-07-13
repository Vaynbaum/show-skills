from pydantic import BaseModel

from models.short_user_model_response import ShortUserModelResponse


class SuggestionInputModel(BaseModel):
    title: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Добавить новый навык",
                "content": "Навык в области программирования, разработка web-приложений",
            }
        }


class SuggestionTickModel(BaseModel):
    completed: bool
    readed: bool

    class Config:
        schema_extra = {
            "example": {
                "completed": True,
                "readed": True,
            }
        }


class SuggestionInDBModel(SuggestionInputModel, SuggestionTickModel):
    key: str = None
    sender: ShortUserModelResponse
