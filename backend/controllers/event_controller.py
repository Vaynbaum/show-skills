from typing import Union
from fastapi import HTTPException

from controllers.user_controller import UserController
from db.database_handler import DatabaseHandler
from exceptions.update_event_exception import UpdateEventException
from handlers.datetime_handler import DatetimeHandler
from models.event_model import EventInDBModel, EventInputModel
from models.response_items import ResponseItems
from models.short_user_model_response import ShortUserModelResponse
from models.message_model import MessageModel


class EventController:
    def __init__(
        self,
        database_controller: DatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)
        self.__datetime_handler = DatetimeHandler()

    async def create_event(self, event: EventInputModel, token: str) -> EventInDBModel:
        """Creating an event

        Args:
            event (EventInputModel): Input event data
            token (str): access token

        Raises:
            HTTPException: If event already exists

        Returns:
            EventInDBModel: Created event
        """
        user = await self.__user_controller.get_user_by_token(token)
        result = await self.__database_controller.get_events_by_query(
            {
                "name": event.name,
                "format_event": event.format_event,
                "place": event.place,
                "author.key": user.key,
                "date": self.__datetime_handler.convert_to_int(event.date),
            }
        )
        if result.count > 0:
            raise HTTPException(status_code=400, detail="Event already exists")
        author = ShortUserModelResponse(**user.dict())
        event = EventInDBModel(**event.dict(), author=author)
        event.date = self.__datetime_handler.convert_to_int(event.date)
        await self.__database_controller.create_event(event)
        return event

    async def get_all_events(
        self, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventInDBModel]:
        """Getting all events from the database

        Args:
            limit (int, optional): Limit of events received. Defaults to 1000.
            last_event_key (str, optional): The last event key received
            in the previous request. Defaults to None.

        Returns:
            ResponseItems[EventInDBModel]: Query result
        """
        return await self.__database_controller.get_events_by_query(
            limit, last_event_key
        )

    async def delete_event(self, key: str) -> MessageModel:
        """Delete a event from the database by key

        Args:
            key (str): event key

        Returns:
            MessageModel
        """
        await self.__database_controller.delete_event_by_key(key)
        return MessageModel(message="Deletion successful")

    async def delete_event_by_user(self, key: str) -> MessageModel:
        """Deleting user events

        Args:
            key (str): user's key

        Raises:
            HTTPException: If events are not deleted

        Returns:
            MessageModel
        """
        events = await self.__database_controller.get_events_by_query(
            query={"author.key": key},
        )
        event_keys = [{"key": event.key} for event in events.items]
        if len(event_keys) > 0:
            result = await self.__database_controller.delete_events_after_user(
                event_keys
            )
            if "failed" in result:
                raise HTTPException(status_code=400, detail="Events not deleted")
        return MessageModel(message="Events deleted successfully")

    async def get_author_key_by_event_key(self, event_key: str) -> str:
        """Getting the event author's key

        Args:
            event_key (str)

        Raises:
            HTTPException: If the event is not found

        Returns:
            str: User's key
        """
        event = await self.__database_controller.get_event_by_key(event_key)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return event.author.key

    async def get_events_by_subscription(
        self,
        token: str,
        next_days: Union[int, None],
        limit: int = 1000,
        last_event_key: str = None,
    ) -> ResponseItems[EventInDBModel]:
        """Getting events by subscriptions

        Args:
            token (str): access token
            next_days (Union[int, None]): The number of days in the future when events will occur
            limit (int, optional): Limit of events received. Defaults to 1000.
            last_event_key (str, optional): The last event key received
            in the previous request. Defaults to None.


        Returns:
            ResponseItems[EventInDBModel]: Query result
        """
        user = await self.__user_controller.get_user_by_token(token)
        if len(user.subscriptions) == 0:
            user_keys = {"author.key": None}
        else:
            if next_days is not None:
                min_date = self.__datetime_handler.now()
                max_date = self.__datetime_handler.now_next_days(next_days)
                user_keys = [
                    {
                        "author.key": subs.favorite.key,
                        "date?lte": max_date,
                        "date?gte": min_date,
                    }
                    for subs in user.subscriptions
                ]
            else:
                user_keys = [
                    {"author.key": subs.favorite.key} for subs in user.subscriptions
                ]
        return await self.__database_controller.get_events_by_query(
            user_keys, limit, last_event_key
        )

    async def get_event_by_user_key(
        self, user_key: str, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventInDBModel]:
        """Getting user events

        Args:
            user_key (str)
            limit (int, optional): Limit of events received. Defaults to 1000.
            last_event_key (str, optional): The last event key received
            in the previous request. Defaults to None.

        Returns:
            ResponseItems[EventInDBModel]: Query result
        """
        return await self.__database_controller.get_events_by_query(
            {"author.key": user_key}, limit, last_event_key
        )

    async def update_event(
        self, event: EventInputModel, event_key: str
    ) -> MessageModel:
        """Updating of event data

        Args:
            event (EventInputModel): input event data
            event_key (str)

        Raises:
            HTTPException: If the event data failed to update

        Returns:
            MessageModel
        """
        try:
            await self.__database_controller.update_event_by_key(event, event_key)
            return MessageModel(message="Editing successful")
        except UpdateEventException as e:

            raise HTTPException(status_code=400, detail=f"{e}")
