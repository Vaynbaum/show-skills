from pydantic import BaseModel
class UnloadContentPostModel(BaseModel):
    name: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Пример названия поста",
                "content": "<h1>Пример</h1>",
            }
        }
