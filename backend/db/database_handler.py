import os
from typing import Union
from deta import Deta
from dotenv import load_dotenv

from db.abstract_database_handler import AbstractDatabaseHandler
from db.handlers.event_database_handler import EventDatabaseHandler
from db.handlers.post_database_handler import PostDatabaseHandler
from db.handlers.role_database_handler import RoleDatabaseHandler
from db.handlers.skill_database_handler import SkillDatabaseHandler
from db.handlers.suggestion_database_handler import SuggetionDatabaseHandler
from db.handlers.user_database_handler import UserDatabaseHandler
from exceptions.append_comment_exception import AppendCommentException
from exceptions.append_like_exception import AppendLikeException
from exceptions.append_links_exception import AppendLinksException
from exceptions.append_skills_exception import AppendSkillsException
from exceptions.update_event_exception import UpdateEventException
from exceptions.update_item_exception import UpdateItemException
from exceptions.update_post_exception import UpdatePostException
from exceptions.update_suggestion_exception import UpdateSuggestionException
from exceptions.update_user_data_exception import UpdateUserDataException
from models.comment_model import CommentModel
from models.event_model import EventInDBModel, EventInputModel
from models.like_model import LikeModel
from models.post_model import PostInDBModel, PostInputModel
from models.response_items import ResponseItems
from models.role_model import RoleInDBModel
from models.skill_model import SkillCreateDataModel, SkillInDBModel
from models.suggestion_model import SuggestionInDBModel, SuggestionTickModel
from models.user_model import UserInDBModel, UserModelResponse


class DatabaseHandler(AbstractDatabaseHandler):
    def __init__(self):
        load_dotenv()
        self.__deta = Deta(os.getenv("DETA_PROJECT_KEY"))
        self.__user_handler = UserDatabaseHandler(self.__deta)
        self.__role_handler = RoleDatabaseHandler(self.__deta)
        self.__skill_handler = SkillDatabaseHandler(self.__deta)
        self.__event_handler = EventDatabaseHandler(self.__deta)
        self.__post_handler = PostDatabaseHandler(self.__deta)
        self.__suggestion_handler = SuggetionDatabaseHandler(self.__deta)

    # User
    async def get_user_by_email(self, email: str) -> Union[UserInDBModel, None]:
        return await self.__user_handler.get_one_by_query({"email": email})

    async def get_user_by_username(self, username: str) -> Union[UserInDBModel, None]:
        return await self.__user_handler.get_one_by_query({"username": username})

    async def get_user_by_key(self, key: str) -> Union[UserInDBModel, None]:
        return await self.__user_handler.get_by_key(key)

    async def get_user_all(
        self, limit: int = 1000, last_user_key: str = None
    ) -> ResponseItems[UserModelResponse]:
        return await self.__user_handler.get_many_by_query(
            limit=limit, last_user_key=last_user_key
        )

    async def put_many_users(self, users: list) -> dict:
        return await self.__user_handler.put_many(users)

    async def create_user(self, data: UserInDBModel) -> Union[UserInDBModel, None]:
        return await self.__user_handler.create(data)

    async def delete_user_by_key(self, key: str) -> None:
        return await self.__user_handler.delete_by_key(key)

    async def append_links_to_user(self, links: list, key: str) -> None:
        try:
            return await self.__user_handler.append_links(links, key)
        except UpdateItemException as e:
            print(e)
            raise AppendLinksException("Adding links to the user is not successful")

    async def append_skills_to_user(self, skills: list, key: str) -> None:
        try:
            return await self.__user_handler.append_skills(skills, key)
        except UpdateItemException as e:
            print(e)
            raise AppendSkillsException("Adding skills to the user is not successful")

    async def update_simple_data_to_user(self, data: dict, key: str) -> None:
        try:
            return await self.__user_handler.simple_data_update(data, key)
        except UpdateItemException as e:
            print(e)
            raise UpdateUserDataException("Updating user data was not successful")

    # Role
    async def get_role_by_name_en(self, name: str) -> Union[RoleInDBModel, None]:
        return await self.__role_handler.get_one_by_query({"name_en": name})

    async def get_role_by_key(self, key: str) -> Union[RoleInDBModel, None]:
        return await self.__role_handler.get_by_key(key)

    async def get_role_all_can_assign(self) -> ResponseItems[RoleInDBModel]:
        return await self.__role_handler.get_many_by_query({"can_assign": True})

    # Skill
    async def create_skill(
        self, data: SkillCreateDataModel
    ) -> Union[SkillInDBModel, None]:
        return await self.__skill_handler.create(data)

    async def get_skill_all(
        self, limit: int = 1000, last_skill_key: str = None
    ) -> ResponseItems[SkillInDBModel]:
        return await self.__skill_handler.get_many_by_query(
            limit=limit, last_skill_key=last_skill_key
        )

    async def get_skill_by_key(self, key: str) -> Union[SkillInDBModel, None]:
        return await self.__skill_handler.get_by_key(key)

    # Event
    async def create_event(self, event: EventInDBModel) -> Union[EventInDBModel, None]:
        return await self.__event_handler.create(event)

    async def get_events_by_query(
        self, query: dict = None, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventInDBModel]:
        return await self.__event_handler.get_many_by_query(
            query, limit, last_event_key
        )

    async def get_all_events(
        self, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventInDBModel]:
        return await self.__event_handler.get_many_by_query(
            limit=limit, last_event_key=last_event_key
        )

    async def delete_event_by_key(self, key: str) -> None:
        return await self.__event_handler.delete(key)

    async def get_event_by_key(self, key: str) -> Union[EventInDBModel, None]:
        return await self.__event_handler.get_by_key(key)

    async def update_event_by_key(self, event: EventInputModel, key: str) -> None:
        try:
            return await self.__event_handler.update(event, key)
        except UpdateItemException as e:
            print(e)
            raise UpdateEventException("Updating event data was not successful")

    async def delete_events_after_user(self, keys: list[dict]) -> dict:
        return await self.__event_handler.delete_after_user(keys)

    # Post
    async def create_post(self, post: PostInDBModel) -> Union[PostInDBModel, None]:
        return await self.__post_handler.create(post)

    async def get_all_posts(
        self, limit: int = 1000, last_post_key: str = None
    ) -> ResponseItems[PostInDBModel]:
        return await self.__post_handler.get_many_by_query(
            limit=limit, last_post_key=last_post_key
        )

    async def get_posts_by_skill(
        self, name_skill: str, limit: int = 1000, last_post_key: str = None
    ) -> ResponseItems[PostInDBModel]:
        return await self.__post_handler.get_many_by_query(
            {"skill.name": name_skill}, limit, last_post_key
        )

    async def get_post_by_key(self, key: str) -> Union[PostInDBModel, None]:
        return await self.__post_handler.get_by_key(key)

    async def delete_post_by_key(self, key: str) -> None:
        return await self.__post_handler.delete_by_key(key)

    async def update_post_by_key(self, post: dict, post_key: str) -> None:
        try:
            return await self.__post_handler.update(post, post_key)
        except UpdateItemException as e:
            print(e)
            raise UpdatePostException("Updating post data was not successful")

    async def append_like_to_post(self, like: LikeModel, post_key: str) -> None:
        try:
            return await self.__post_handler.append_like(like, post_key)
        except UpdateItemException as e:
            print(e)
            raise AppendLikeException("Adding like to post is not successful")

    async def append_comment_to_post(
        self, comment: CommentModel, post_key: str
    ) -> None:
        try:
            return await self.__post_handler.append_comment(comment, post_key)
        except UpdateItemException as e:
            print(e)
            raise AppendCommentException("Adding comment to post is not successful")

    # Suggestion
    async def add_suggestion(
        self, suggestion: SuggestionInDBModel
    ) -> Union[SuggestionInDBModel, None]:
        return await self.__suggestion_handler.add(suggestion)

    async def get_all_suggestions(
        self, query: dict, limit: int = 1000, last_key: str = None
    ) -> ResponseItems[SuggestionInDBModel]:
        return await self.__suggestion_handler.get_many_by_query(query, limit, last_key)

    async def update_suggestion(
        self, data: dict, suggestion_key: str
    ) -> None:
        try:
            return await self.__suggestion_handler.update(data, suggestion_key)
        except UpdateItemException as e:
            print(e)
            raise UpdateSuggestionException("Updating suggestion data was not successful")
