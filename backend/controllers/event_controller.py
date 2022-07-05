from fastapi import HTTPException
from datetime import datetime, timedelta

from controllers.user_controller import UserController
from db.abstract_database_handler import AbstractDatabaseHandler
from models.event_model import EventModelInDB, EventModelInput
from models.items import ResponseItems
from models.short_response_user_model import ShortResponseUserModel
from models.message_model import MessageModel


class EventController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)

    async def create_event(self, event: EventModelInput, token: str):
        user = await self.__user_controller.get_user_by_token(token)
        result = await self.__database_controller.get_event_by_query(
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
        author = ShortResponseUserModel(**user.dict())
        event = EventModelInDB(**event.dict(), author=author)
        await self.__database_controller.create_event(event)
        return MessageModel(message="Event successful created")

    async def get_all_events(self):
        return await self.__database_controller.get_all_events()

    async def delete_event(self, key: str) -> MessageModel:
        await self.__database_controller.delete_event_by_key(key)
        return MessageModel(message="Deletion successful")

    async def get_key_author_by_event_key(self, event_key: str) -> str:
        event = await self.__database_controller.get_event_by_key(event_key)
        if event is None:
            raise HTTPException(status_code=400, detail="Event not found")
        return event.author.key

    async def get_events_by_subscription(
        self, next_days, token
    ) -> ResponseItems[EventModelInDB]:
        user = await self.__user_controller.get_user_by_token(token)
        if len(user.subscriptions) == 0:
            user_keys = {"author.key": None}
        else:
            if next_days is not None:
                min_date = (datetime.now()).timestamp()
                max_date = (datetime.now() + timedelta(days=next_days)).timestamp()
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
        return await self.__database_controller.get_event_by_query(user_keys)

    async def get_event_by_user_key(
        self, user_key: str
    ) -> ResponseItems[EventModelInDB]:
        return await self.__database_controller.get_event_by_query(
            {"author.key": user_key}
        )

    async def update_event(self, event: EventModelInput, event_key: str):
        await self.__database_controller.update_event_by_key(event, event_key)
        return MessageModel(message="Editing successful")
