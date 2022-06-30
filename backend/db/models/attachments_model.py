from pydantic import BaseModel
from datetime import datetime


class AttachmentModel(BaseModel):
    key: str | None
    url: str
    creator_key: str
