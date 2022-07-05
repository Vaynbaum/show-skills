from typing import Union

from pydantic import BaseModel


class ShortResponseUserModel(BaseModel):
    username: str
    lastname: str
    key: Union[str, None]
    firstname: str
    url_photo: Union[str, None]