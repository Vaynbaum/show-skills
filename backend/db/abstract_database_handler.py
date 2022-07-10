from abc import ABC, abstractmethod
from typing import Union
from models.comment_model import CommentModel
from models.event_model import EventInDBModel, EventInputModel
from models.like_model import LikeModel
from models.post_model import PostInDBModel
from models.response_items import ResponseItems

from models.role_model import RoleInDBModel
from models.skill_model import SkillCreateDataModel, SkillInDBModel
from models.suggestion_model import SuggestionInDBModel, SuggestionTickModel
from models.user_model import UserInDBModel, UserModelResponse


class AbstractDatabaseHandler(ABC):

    # User
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Union[UserInDBModel, None]:
        """Get one user by email from the database

        Args:
            email (str): User's email

        Returns:
            Union[UserInDBModel, None]: If a user is found, then returns UserInDBModel otherwise None
        """
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Union[UserInDBModel, None]:
        """Get one user by username from the database

        Args:
            username (str): User's username

        Returns:
            Union[UserInDBModel, None]: If a user is found, then returns UserInDBModel otherwise None
        """
        pass

    @abstractmethod
    async def get_user_by_key(self, key: str) -> Union[UserInDBModel, None]:
        """Get a user by key from the database

        Args:
            key (str): The user's key in the database

        Returns:
            Union[UserInDBModel, None]: If a user is found, then returns UserInDBModel otherwise None"""
        pass

    @abstractmethod
    async def get_user_all(
        self, limit: int = 1000, last_user_key: str = None
    ) -> ResponseItems[UserModelResponse]:
        """Get all users in the database

        Args:
            limit (int, optional): Limit of users received. Defaults to 1000.
            last_user_key (str, optional): The last user key received in the previous request. Defaults to None.

        Returns:
            ResponseItems[UserModelResponse]: Query result
        """
        pass

    @abstractmethod
    async def put_many_users(self, users: list) -> dict:
        """Put multiple users in the database

        Args:
            users (list): List of users

        Returns:
            dict: Returns a dict with "processed" and "failed"(if any) items"""
        pass

    @abstractmethod
    async def create_user(self, user: UserInDBModel) -> Union[UserInDBModel, None]:
        """Adding a new user to the database

        Args:
            user (UserInDBModel): New user model

        Returns:
            Union[UserInDBModel, None]: The model of the user added to the database otherwise None
        """
        pass

    @abstractmethod
    async def delete_user_by_key(self, key: str) -> None:
        """Delete a user from the database by key

        Args:
            key (str): The user's key in the database

        Returns:
            None: Returns nothing
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    # Role
    @abstractmethod
    async def get_role_by_name_en(self, name: str) -> Union[RoleInDBModel, None]:
        """Get one role by name from the database

        Args:
            name (str): role name

        Returns:
            Union[RoleInDBModel, None]: If a role is found, then returns RoleInDBModel otherwise None
        """
        pass

    @abstractmethod
    async def get_role_by_key(self, key: str) -> Union[RoleInDBModel, None]:
        """Get a role by key from the database

        Args:
            key (str): The role key in the database

        Returns:
            Union[RoleInDBModel, None]: If a role is found, then returns RoleInDBModel otherwise None
        """
        pass

    @abstractmethod
    async def get_role_all_can_assign(self) -> ResponseItems[RoleInDBModel]:
        """Get all the roles that can be assigned to a user from the database

        Returns:
            ResponseItems[RoleInDBModel]: Query result
        """
        pass

    # Skill
    @abstractmethod
    async def create_skill(
        self, data: SkillCreateDataModel
    ) -> Union[SkillInDBModel, None]:
        """Adding a new skill to the database

        Args:
            data (SkillCreateDataModel): New skill model

        Returns:
            Union[SkillInDBModel, None]: The model of the skill added to the database otherwise None
        """
        pass

    @abstractmethod
    async def get_skill_all(
        self, limit: int = 1000, last_skill_key: str = None
    ) -> ResponseItems[SkillInDBModel]:
        """Get all skills in the database

        Args:
            limit (int, optional): Limit of skills received. Defaults to 1000.
            last_user_key (str, optional): The last skill key received in the previous request. Defaults to None.

        Returns:
            ResponseItems[SkillInDBModel]: Query result
        """
        pass

    @abstractmethod
    async def get_skill_by_key(self, key: str) -> Union[SkillInDBModel, None]:
        """Get a skill by key from the database

        Args:
            key (str): The skill key in the database

        Returns:
            Union[SkillInDBModel, None]: If a skill is found, then returns SkillInDBModel otherwise None"""
        pass

    # Event
    @abstractmethod
    async def create_event(self, event: EventInDBModel) -> Union[EventInDBModel, None]:
        """Adding a new event to the database

        Args:
            event (EventInDBModel): New event model

        Returns:
            Union[EventInDBModel, None]: The model of the event added to the database otherwise None
        """
        pass

    @abstractmethod
    async def get_events_by_query(
        self, query: dict = None, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventInDBModel]:
        """Get events by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.
            limit (int, optional): Limit of events received. Defaults to 1000.
            last_event_key (str, optional): The last event key received in the previous request. Defaults to None.

        Returns:
            ResponseItems[EventInDBModel]: Query result
        """
        pass

    @abstractmethod
    async def get_all_events(
        self, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventInDBModel]:
        """Get all events from the database

        Args:
            limit (int, optional): Limit of events received. Defaults to 1000.
            last_event_key (str, optional): The last event key received in the previous request.
            Defaults to None.

        Returns:
            ResponseItems[EventInDBModel]: Query result
        """
        pass

    @abstractmethod
    async def delete_event_by_key(self, key: str) -> None:
        """Delete a event from the database by key

        Args:
            key (str): The event key in the database

        Returns:
            None: Returns nothing
        """
        pass

    @abstractmethod
    async def get_event_by_key(self, key: str) -> Union[EventInDBModel, None]:
        """Get a event by key from the database

        Args:
            key (str): The event key in the database

        Returns:
            Union[EventInDBModel, None]: If a event is found, then returns EventInDBModel otherwise None
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def delete_events_after_user(self, keys: list[dict]) -> dict:
        pass

    # Post
    @abstractmethod
    async def create_post(self, post: PostInDBModel) -> Union[PostInDBModel, None]:
        """Adding a new post to the database

        Args:
            post (PostInDBModel): New post model

        Returns:
            Union[PostInDBModel, None]: The model of the post added to the database otherwise None
        """
        pass

    @abstractmethod
    async def get_all_posts(
        self, limit: int = 1000, last_post_key: str = None
    ) -> ResponseItems[PostInDBModel]:
        pass

    @abstractmethod
    async def get_posts_by_skill(
        name_skill: str, limit: int = 1000, last_post_key: str = None
    ) -> ResponseItems[PostInDBModel]:
        pass

    @abstractmethod
    async def get_post_by_key(self, key: str) -> Union[PostInDBModel, None]:
        pass

    @abstractmethod
    async def delete_post_by_key(self, key: str) -> None:
        pass

    @abstractmethod
    async def update_post_by_key(self, post: dict, post_key: str) -> None:
        pass

    @abstractmethod
    async def append_like_to_post(self, like: LikeModel, post_key: str) -> None:
        pass

    @abstractmethod
    async def append_comment_to_post(
        self, comment: CommentModel, post_key: str
    ) -> None:
        pass

    # Suggestoin
    @abstractmethod
    async def add_suggestion(
        self, suggestion: SuggestionInDBModel
    ) -> Union[SuggestionInDBModel, None]:
        pass

    @abstractmethod
    async def get_all_suggestions(
        self, query: dict, limit: int = 1000, last_key: str = None
    ) -> ResponseItems[SuggestionInDBModel]:
        pass

    @abstractmethod
    async def update_suggestion(self, data: dict, suggestion_key: str) -> None:
        pass
