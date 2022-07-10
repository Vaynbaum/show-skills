from datetime import timedelta
from typing import Union
from deta import Deta

from exceptions.update_item_exception import UpdateItemException
from handlers.datetime_handler import DatetimeHandler
from models.event_model import EventInDBModel, EventInputModel
from models.response_items import ResponseItems


class EventDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__event_db = deta.AsyncBase("events")
        self.__datetime_handler = DatetimeHandler()

    async def get_many_by_query(
        self, query: dict = None, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventInDBModel]:
        """Get events by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.
            limit (int, optional): Limit of events received. Defaults to 1000.
            last_event_key (str, optional): The last event key received in the previous request.
            Defaults to None.

        Returns:
            ResponseItems[EventInDBModel]: Query result
        """
        result = await self.__event_db.fetch(query, limit=limit, last=last_event_key)
        return ResponseItems[EventInDBModel](
            count=result.count, last=result.last, items=result.items
        )

    async def create(self, event: EventInDBModel) -> Union[EventInDBModel, None]:
        """Adding a new event to the database

        Args:
            event (EventInDBModel): New event model

        Returns:
            Union[EventInDBModel, None]: The model of the event added to the database otherwise None
        """
        try:
            event = await self.__event_db.put(
                data=event.dict(),
                expire_at=self.__datetime_handler.add_timedelta(
                    event.date, timedelta(minutes=20)
                ),
            )
            return EventInDBModel(**event)
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

    async def get_by_key(self, key: str) -> Union[EventInDBModel, None]:
        """Get a event by key from the database

        Args:
            key (str): The event key in the database

        Returns:
            Union[EventInDBModel, None]: If a event is found,
            then returns EventInDBModel otherwise None
        """
        event = await self.__event_db.get(key)
        return EventInDBModel(**event) if event is not None else None

    async def update(self, event: EventInputModel, key: str) -> None:
        """Updating of event data

        Args:
            event (EventInputModel): event data
            key (str): The event key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        expire = self.__datetime_handler.add_timedelta(
            event.date, timedelta(minutes=20)
        )
        try:
            return await self.__event_db.update(
                event.dict(),
                key,
                expire_at=expire,
            )
        except BaseException as e:
            print(e)
            raise UpdateItemException("Updating data was not successful")

    async def delete_after_user(self, keys: list[dict]):
        return await self.__event_db.put_many(keys, expire_in=5)
