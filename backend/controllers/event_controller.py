from fastapi import HTTPException

from controllers.user_controller import UserController
from db.abstract_database_handler import AbstractDatabaseHandler
from exceptions.update_event_exception import UpdateEventException
from handlers.datetime_handler import DatetimeHandler
from models.event_model import EventInDBModel, EventInputModel
from models.response_items import ResponseItems
from models.short_user_model_response import ShortUserModelResponse
from models.message_model import MessageModel


class EventController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)
        self.__datetime_handler = DatetimeHandler()

    async def create_event(self, event: EventInputModel, token: str):
        user = await self.__user_controller.get_user_by_token(token)
        result = await self.__database_controller.get_events_by_query(
            {
                "name": event.name,
                "format_event": event.format_event,
                "place": event.place,
                "author.key": user.key,
                "date": event.date,
            }
        )
        if result.count > 0:
            raise HTTPException(status_code=400, detail="Event already exists")
        author = ShortUserModelResponse(**user.dict())
        event = EventInDBModel(**event.dict(), author=author)
        await self.__database_controller.create_event(event)
        return MessageModel(message="Event successful created")

    async def get_all_events(self, limit: int = 1000, last_event_key: str = None):
        return await self.__database_controller.get_all_events(limit, last_event_key)

    async def delete_event(self, key: str) -> MessageModel:
        await self.__database_controller.delete_event_by_key(key)
        return MessageModel(message="Deletion successful")

    async def delete_event_by_user(self, key: str) -> None:
        events = await self.__database_controller.get_events_by_query(
            {"author.key": key},
        )
        event_keys = [{"key": event.key} for event in events.items]
        result = await self.__database_controller.delete_events_after_user(event_keys)
        if "failed" in result:
            raise HTTPException(status_code=400, detail="Events not deleted")

    async def get_author_key_by_event_key(self, event_key: str) -> str:
        event = await self.__database_controller.get_event_by_key(event_key)
        if event is None:
            raise HTTPException(status_code=400, detail="Event not found")
        return event.author.key

    async def get_events_by_subscription(
        self,
        token: str,
        limit: int = 1000,
        last_event_key: str = None,
        next_days: int = None,
    ) -> ResponseItems[EventInDBModel]:
        user = await self.__user_controller.get_user_by_token(token)
        if len(user.subscriptions) == 0:
            user_keys = {"author.key": None}
        else:
            if next_days is not None:
                min_date = self.__datetime_handler.now()
                max_date = self.__datetime_handler.now_next_days(days=next_days)
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
        return await self.__database_controller.get_events_by_query(
            {"author.key": user_key}, limit, last_event_key
        )

    async def update_event(self, event: EventInputModel, event_key: str):
        try:
            await self.__database_controller.update_event_by_key(event, event_key)
            return MessageModel(message="Editing successful")
        except UpdateEventException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")
