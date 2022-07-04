from typing import Generic, TypeVar, List, Union
from pydantic.generics import GenericModel

Item = TypeVar("Item")


class ResponseItems(GenericModel, Generic[Item]):
    items: List[Item]
    count: int
    last: Union[str, None]
