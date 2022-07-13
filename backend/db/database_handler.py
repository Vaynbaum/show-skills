import os
from typing import Union
from deta import Deta
from dotenv import load_dotenv

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
from models.post_model import PostInDBModel
from models.response_items import ResponseItems
from models.role_model import RoleInDBModel
from models.skill_model import SkillCreateDataModel, SkillInDBModel
from models.suggestion_model import SuggestionInDBModel
from models.user_model import UserInDBModel, UserModelResponse


class DatabaseHandler():
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
        """Get one user by email from the database

        Args:
            email (str): User's email

        Returns:
            Union[UserInDBModel, None]: If a user is found,
            then returns UserInDBModel otherwise None
        """
        return await self.__user_handler.get_one_by_query({"email": email})

    async def get_user_by_username(self, username: str) -> Union[UserInDBModel, None]:
        """Get one user by username from the database

        Args:
            username (str): User's username

        Returns:
            Union[UserInDBModel, None]: If a user is found,
            then returns UserInDBModel otherwise None
        """
        return await self.__user_handler.get_one_by_query({"username": username})

    async def get_user_by_key(self, key: str) -> Union[UserInDBModel, None]:
        """Get a user by key from the database

        Args:
            key (str): The user's key in the database

        Returns:
            Union[UserInDBModel, None]: If a user is found,
            then returns UserInDBModel otherwise None"""
        return await self.__user_handler.get_by_key(key)

    async def get_user_all(
        self, limit: int, last_user_key: str
    ) -> ResponseItems[UserModelResponse]:
        """Get all users in the database

        Args:
            limit (int): Limit of users received
            last_user_key (str): The last user key received in the previous request

        Returns:
            ResponseItems[UserModelResponse]: Query result
        """
        return await self.__user_handler.get_many_by_query(limit, last_user_key)

    async def put_many_users(self, users: list) -> dict:
        """Put multiple users in the database

        Args:
            users (list): List of users

        Returns:
            dict: Returns a dict with "processed" and "failed"(if any) items
        """
        return await self.__user_handler.put_many(users)

    async def create_user(self, data: UserInDBModel) -> Union[UserInDBModel, None]:
        """Adding a new user to the database

        Args:
            user (UserInDBModel): New user model

        Returns:
            Union[UserInDBModel, None]: The model of the user added
            to the database otherwise None
        """
        return await self.__user_handler.create(data)

    async def delete_user_by_key(self, key: str) -> None:
        """Delete a user from the database by key

        Args:
            key (str): The user's key in the database

        Returns:
            None: Returns nothing
        """
        return await self.__user_handler.delete_by_key(key)

    async def append_links_to_user(self, links: list, key: str) -> None:
        """Add links to the user

        Args:
            links (list): List of links
            key (str): The user's key in the database

        Raises:
            AppendLinksException: If it is not successful to add links to the user

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__user_handler.append_links(links, key)
        except UpdateItemException as e:
            
            raise AppendLinksException("Adding links to the user is not successful")

    async def append_skills_to_user(self, skills: list, key: str) -> None:
        """Add skills to the user

        Args:
            skills (list): List of skills
            key (str): The user's key in the database

        Raises:
            AppendSkillsException: If it is not successful to add skills to the user

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__user_handler.append_skills(skills, key)
        except UpdateItemException as e:
            
            raise AppendSkillsException("Adding skills to the user is not successful")

    async def update_simple_data_to_user(self, data: dict, key: str) -> None:
        """Simple updating of user data

        Args:
            data (dict): user data
            key (str): The user's key in the database

        Raises:
            UpdateUserDataException: If the user data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__user_handler.simple_data_update(data, key)
        except UpdateItemException as e:
            
            raise UpdateUserDataException("Updating user data was not successful")

    # Role
    async def get_role_by_name_en(self, name: str) -> Union[RoleInDBModel, None]:
        """Get one role by name from the database

        Args:
            name (str): role name

        Returns:
            Union[RoleInDBModel, None]: If a role is found,
            then returns RoleInDBModel otherwise None
        """
        return await self.__role_handler.get_one_by_query({"name_en": name})

    async def get_role_by_key(self, key: str) -> Union[RoleInDBModel, None]:
        """Get a role by key from the database

        Args:
            key (str): The role key in the database

        Returns:
            Union[RoleInDBModel, None]: If a role is found,
            then returns RoleInDBModel otherwise None
        """
        return await self.__role_handler.get_by_key(key)

    async def get_role_all_can_assign(self) -> ResponseItems[RoleInDBModel]:
        """Get all the roles that can be assigned to a user from the database

        Returns:
            ResponseItems[RoleInDBModel]: Query result
        """
        return await self.__role_handler.get_many_by_query({"can_assign": True})

    # Skill
    async def create_skill(
        self, data: SkillCreateDataModel
    ) -> Union[SkillInDBModel, None]:
        """Adding a new skill to the database

        Args:
            data (SkillCreateDataModel): New skill model

        Returns:
            Union[SkillInDBModel, None]: The model of the skill added
            to the database otherwise None
        """
        return await self.__skill_handler.create(data)

    async def get_skill_all(
        self, limit: int, last_skill_key: str
    ) -> ResponseItems[SkillInDBModel]:
        """Get all skills in the database

        Args:
            limit (int): Limit of skills received
            last_skill_key (str): The last skill key received in the previous request

        Returns:
            ResponseItems[SkillInDBModel]: Query result
        """
        return await self.__skill_handler.get_many_by_query(limit, last_skill_key)

    async def get_skill_by_key(self, key: str) -> Union[SkillInDBModel, None]:
        """Get a skill by key from the database

        Args:
            key (str): The skill key in the database

        Returns:
            Union[SkillInDBModel, None]: If a skill is found,
            then returns SkillInDBModel otherwise None
        """
        return await self.__skill_handler.get_by_key(key)

    # Event
    async def create_event(self, event: EventInDBModel) -> Union[EventInDBModel, None]:
        """Adding a new event to the database

        Args:
            event (EventInDBModel): New event model

        Returns:
            Union[EventInDBModel, None]: The model of the event added
            to the database otherwise None
        """
        return await self.__event_handler.create(event)

    async def get_events_by_query(
        self, limit: int, last_event_key: str, query: dict = None
    ) -> ResponseItems[EventInDBModel]:
        """Get events by different criteria from the database

        Args:
            limit (int): Limit of events received
            last_event_key (str): The last event key received in the previous request
            query (dict, optional): Choosing criteria. Defaults to None

        Returns:
            ResponseItems[EventInDBModel]: Query result
        """
        return await self.__event_handler.get_many_by_query(
            limit, last_event_key, query
        )

    async def delete_event_by_key(self, key: str) -> None:
        """Delete a event from the database by key

        Args:
            key (str): The event key in the database

        Returns:
            None: Returns nothing
        """
        return await self.__event_handler.delete(key)

    async def get_event_by_key(self, key: str) -> Union[EventInDBModel, None]:
        """Get a event by key from the database

        Args:
            key (str): The event key in the database

        Returns:
            Union[EventInDBModel, None]: If a event is found,
            then returns EventInDBModel otherwise None
        """
        return await self.__event_handler.get_by_key(key)

    async def update_event_by_key(self, event: EventInputModel, key: str) -> None:
        """Updating of event data

        Args:
            event (EventInputModel): event data
            key (str): The event key in the database

        Raises:
            UpdateEventException: If the event data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__event_handler.update(event, key)
        except UpdateItemException as e:
            
            raise UpdateEventException("Updating event data was not successful")

    async def delete_events_after_user(self, keys: list[dict]) -> dict:
        """Deleting events by keys

        Args:
            keys (list[dict]): List of event keys

        Returns:
            dict: Returns a dict with processed and failed(if any) items
        """
        return await self.__event_handler.delete_after_user(keys)

    # Post
    async def create_post(self, post: PostInDBModel) -> Union[PostInDBModel, None]:
        """Adding a new post to the database

        Args:
            post (PostInDBModel): New post model

        Returns:
            Union[PostInDBModel, None]: The model of the post added
            to the database otherwise None
        """
        return await self.__post_handler.create(post)

    async def get_posts_by_query(
        self, limit: int, last_post_key: str, query: dict = None
    ) -> ResponseItems[PostInDBModel]:
        """Get posts by different criteria from the database

        Args:
            limit (int): Limit of posts received
            last_post_key (str): The last post key received in the previous request
            query (dict, optional): Choosing criteria. Defaults to None

        Returns:
            ResponseItems[PostInDBModel]: Query result
        """
        return await self.__post_handler.get_many_by_query(limit, last_post_key, query)

    async def get_post_by_key(self, key: str) -> Union[PostInDBModel, None]:
        """Get post by key from the database

        Args:
            key (str): The post key in the database

        Returns:
            Union[PostInDBModel, None]: If a post is found,
            then returns PostInDBModel otherwise None
        """
        return await self.__post_handler.get_by_key(key)

    async def delete_post_by_key(self, key: str) -> None:
        """Delete a post from the database by key

        Args:
            key (str): The post key in the database

        Returns:
            None: Returns nothing
        """
        return await self.__post_handler.delete_by_key(key)

    async def update_post_by_key(self, post: dict, post_key: str) -> None:
        """Updating of post data

        Args:
            post (dict): post data
            post_key (str): The post key in the database

        Raises:
            UpdatePostException: If the post data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__post_handler.update(post, post_key)
        except UpdateItemException as e:
            
            raise UpdatePostException("Updating post data was not successful")

    async def append_like_to_post(self, like: LikeModel, post_key: str) -> None:
        """Add like to the post

        Args:
            like (LikeModel)
            post_key (str): The post key in the database

        Raises:
            AppendLikeException: If it is not successful to add like to the post

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__post_handler.append_like(like, post_key)
        except UpdateItemException as e:
            
            raise AppendLikeException("Adding like to post is not successful")

    async def append_comment_to_post(
        self, comment: CommentModel, post_key: str
    ) -> None:
        """Add comment to post

        Args:
            comment (CommentModel): comment model
            post_key (str): post key in the database

        Raises:
            AppendCommentException: If it is not successful to add comment to the post

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__post_handler.append_comment(comment, post_key)
        except UpdateItemException as e:
            
            raise AppendCommentException("Adding comment to post is not successful")

    # Suggestion
    async def add_suggestion(
        self, suggestion: SuggestionInDBModel
    ) -> Union[SuggestionInDBModel, None]:
        """Adding a new suggestion to the database

        Args:
            suggestion (SuggestionInDBModel): New suggestion model

        Returns:
            Union[SuggestionInDBModel, None]: The model of the suggestion added 
            to the database otherwise None
        """
        return await self.__suggestion_handler.add(suggestion)

    async def get_all_suggestions(
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
        return await self.__suggestion_handler.get_many_by_query(query, limit, last_key)

    async def update_suggestion(self, data: dict, suggestion_key: str) -> None:
        """Updating of suggestion data

        Args:
            data (dict): suggestion data
            suggestion_key (str): The suggestion key in the database

        Raises:
            UpdateSuggestionException: If the suggestion data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__suggestion_handler.update(data, suggestion_key)
        except UpdateItemException as e:
            
            raise UpdateSuggestionException(
                "Updating suggestion data was not successful"
            )
