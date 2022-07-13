from typing import Union
from deta import Deta
from exceptions.update_item_exception import UpdateItemException
from models.response_items import ResponseItems

from models.suggestion_model import SuggestionInDBModel


class SuggetionDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__suggestions_db = deta.AsyncBase("suggestions")

    async def add(
        self, suggestion: SuggestionInDBModel
    ) -> Union[SuggestionInDBModel, None]:
        """Adding a new suggestion to the database

        Args:
            suggestion (SuggestionInDBModel): New suggestion model

        Returns:
            Union[SuggestionInDBModel, None]: The model of the suggestion
            added to the database otherwise None
        """
        try:
            suggestion = await self.__suggestions_db.put(suggestion.dict())
            return SuggestionInDBModel(**suggestion)
        except:
            return None

    async def get_many_by_query(
        self, query: dict, limit: int, last_key: str
    ) -> ResponseItems[SuggestionInDBModel]:
        """Get suggestions by different criteria from the database

        Args:
            query (dict): Choosing criteria
            limit (int): Limit of suggestions received
            last_key (str): The last suggestion key received in the previous request

        Returns:
            ResponseItems[SuggestionInDBModel]: Query result
        """
        result = await self.__suggestions_db.fetch(query, limit=limit, last=last_key)
        return ResponseItems[SuggestionInDBModel](
            count=result.count, last=result.last, items=result.items
        )

    async def update(self, suggestion: dict, suggestion_key: str) -> None:
        """Updating of suggestion data

        Args:
            suggestion (dict): suggestion data
            suggestion_key (str): The suggestion key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__suggestions_db.update(suggestion, suggestion_key)
        except BaseException as e:
            
            raise UpdateItemException("Updating data was not successful")
