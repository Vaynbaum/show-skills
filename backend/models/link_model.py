from pydantic import BaseModel


class LinkModel(BaseModel):
    name: str
    url: str

    class Config:
        schema_extra = {"example": {"name": "VK", "url": "https://example"}}
