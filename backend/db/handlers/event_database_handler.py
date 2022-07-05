from datetime import datetime, timedelta
from deta import Deta

from models.event_model import EventModelInDB, EventModelInput


class EventDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__event_db = deta.AsyncBase("events")

    async def get_by_query(self, query):
        return await self.__event_db.fetch(query)

    async def create(self, event: EventModelInDB):
        expire = datetime.utcfromtimestamp(event.date) + timedelta(minutes=20)
        return await self.__event_db.put(data=event.dict(), expire_at=expire)

    async def delete(self, key: str):
        return await self.__event_db.delete(key)

    async def get_by_key(self, key: str):
        return await self.__event_db.get(key)

    async def update(self, event: EventModelInput, key: str):
        return await self.__event_db.update(event.dict(), key)

    # async def delete_after_user(self,key_user: str):
    #     return await self.__event_db.put_many({"key"}, key)
