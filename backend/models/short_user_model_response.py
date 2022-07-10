from typing import Union

from pydantic import BaseModel


class ShortUserModelResponse(BaseModel):
    username: str
    firstname: str
    lastname: str
    key: Union[str, None]
    url: Union[str, None]