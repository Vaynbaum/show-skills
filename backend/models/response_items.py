from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel

Item = TypeVar("Item")


class ResponseItems(GenericModel, Generic[Item]):
    items: List[Item]
    count: int
    last: str = None
