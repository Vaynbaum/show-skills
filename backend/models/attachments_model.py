from typing import Union
from pydantic import BaseModel


class AttachmentModel(BaseModel):
    key: Union[str, None]
    url: str
    creator_key: str
