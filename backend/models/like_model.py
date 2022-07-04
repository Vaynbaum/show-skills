from typing import Union
from pydantic import BaseModel


class LikeModel(BaseModel):
    key: Union[str, None]
    # type_object: int
    user_key: str
    post_key: str
