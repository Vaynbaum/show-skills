from fastapi import HTTPException

from controllers.user_controller import UserController
from db.abstract_database_handler import AbstractDatabaseHandler
from models.link_model import LinkModel
from models.message_model import MessageModel


class LinkController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)

    async def add_link(self, link: LinkModel, token):
        user = await self.__user_controller.get_user_by_token(token)
        result = list(filter(lambda item: link.url == item.url, user.links))
        if len(result) > 0:
            raise HTTPException(status_code=400, detail="Link already exists")
        else:
            await self.__database_controller.append_links_to_user(
                [link.dict()], user.key
            )
            return MessageModel(message="Link successfully added")

    async def remove_link(self, url_link, token):
        user = await self.__user_controller.get_user_by_token(token)
        result_find = list(filter(lambda item: url_link == item.url, user.links))
        if len(result_find) > 0:
            user.links.remove(result_find[0])
            await self.__database_controller.update_simple_data_to_user(
                {"links": (user.dict())["links"]}, user.key
            )
            return MessageModel(message="Link successfully removed")
        else:
            raise HTTPException(status_code=400, detail="Link not found")
