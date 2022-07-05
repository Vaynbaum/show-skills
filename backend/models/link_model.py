from pydantic import BaseModel


class LinkModel(BaseModel):
    name: str
    url: str
