from pydantic import BaseModel


class MessageModel(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {"message": "The action was successfully completed"},
        }