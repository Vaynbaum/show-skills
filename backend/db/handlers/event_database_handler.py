from datetime import datetime, timedelta
from typing import Union
from deta import Deta
from exceptions.update_item_exception import UpdateItemException

from models.event_model import EventModelInDB, EventModelInput
from models.response_items import ResponseItems


class EventDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__event_db = deta.AsyncBase("events")

    async def get_many_by_query(
        self, query: dict = None, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventModelInDB]:
        """Get events by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.
            limit (int, optional): Limit of events received. Defaults to 1000.
            last_event_key (str, optional): The last event key received in the previous request. Defaults to None.

        Returns:
            ResponseItems[EventModelInDB]: Query result
        """
        result = await self.__event_db.fetch(query, limit, last_event_key)
        return ResponseItems[EventModelInDB](
            count=result.count, last=result.last, items=result.items
        )

    async def create(self, event: EventModelInDB) -> Union[EventModelInDB, None]:
        """Adding a new event to the database

        Args:
            event (EventModelInDB): New event model

        Returns:
            Union[EventModelInDB, None]: The model of the event added to the database otherwise None
        """
        expire = datetime.utcfromtimestamp(event.date) + timedelta(minutes=20)
        try:
            event = await self.__event_db.put(data=event.dict(), expire_at=expire)
            return EventModelInDB(**event)
        except:
            return None

    async def delete(self, key: str) -> None:
        """Delete a event from the database by key

        Args:
            key (str): The event key in the database

        Returns:
            None: Returns nothing
        """
        return await self.__event_db.delete(key)

    async def get_by_key(self, key: str) -> Union[EventModelInDB, None]:
        """Get a event by key from the database

        Args:
            key (str): The event key in the database

        Returns:
            Union[EventModelInDB, None]: If a event is found, then returns EventModelInDB otherwise None
        """
        event = await self.__event_db.get(key)
        return EventModelInDB(**event) if event is not None else None

    async def update(self, event: EventModelInput, key: str) -> None:
        """Updating of event data

        Args:
            event (EventModelInput): event data
            key (str): The event key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__event_db.update(event.dict(), key)
        except BaseException as e:
            print(e)
            raise UpdateItemException("Updating data was not successful")

    # async def delete_after_user(self,key_user: str):
    #     return await self.__event_db.put_many({"key"}, key)
