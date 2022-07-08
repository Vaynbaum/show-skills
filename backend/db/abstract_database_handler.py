from abc import ABC, abstractmethod
from typing import Union
from models.event_model import EventModelInDB, EventModelInput
from models.response_items import ResponseItems

from models.role_model import RoleModelInDB
from models.skill_model import SkillCreateDataModel, SkillModelInDB
from models.user_model import UserModelInDB, UserModelResponse


class AbstractDatabaseHandler(ABC):

    # User
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Union[UserModelInDB, None]:
        """Get one user by email from the database

        Args:
            email (str): User's email

        Returns:
            Union[UserModelInDB, None]: If a user is found, then returns UserModelInDB otherwise None
        """
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Union[UserModelInDB, None]:
        """Get one user by username from the database

        Args:
            username (str): User's username

        Returns:
            Union[UserModelInDB, None]: If a user is found, then returns UserModelInDB otherwise None
        """
        pass

    @abstractmethod
    async def get_user_by_key(self, key: str) -> Union[UserModelInDB, None]:
        """Get a user by key from the database

        Args:
            key (str): The user's key in the database

        Returns:
            Union[UserModelInDB, None]: If a user is found, then returns UserModelInDB otherwise None"""
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
    async def create_user(self, user: UserModelInDB) -> Union[UserModelInDB, None]:
        """Adding a new user to the database

        Args:
            user (UserModelInDB): New user model

        Returns:
            Union[UserModelInDB, None]: The model of the user added to the database otherwise None
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
    async def simple_data_update_to_user(self, data: dict, key: str) -> None:
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
    async def get_role_by_name_en(self, name: str) -> Union[RoleModelInDB, None]:
        """Get one role by name from the database

        Args:
            name (str): role name

        Returns:
            Union[RoleModelInDB, None]: If a role is found, then returns RoleModelInDB otherwise None
        """
        pass

    @abstractmethod
    async def get_role_by_key(self, key: str) -> Union[RoleModelInDB, None]:
        """Get a role by key from the database

        Args:
            key (str): The role key in the database

        Returns:
            Union[RoleModelInDB, None]: If a role is found, then returns RoleModelInDB otherwise None
        """
        pass

    @abstractmethod
    async def get_role_all_can_assign(
        self, limit: int = 1000, last_role_key: str = None
    ) -> ResponseItems[RoleModelInDB]:
        """Get all the roles that can be assigned to a user from the database

        Args:
            limit (int, optional): Limit of roles received. Defaults to 1000.
            last_role_key (str, optional): The last role key received in the previous request.
            Defaults to None.

        Returns:
            ResponseItems[RoleModelInDB]: Query result
        """
        pass

    # Skill
    @abstractmethod
    async def create_skill(
        self, data: SkillCreateDataModel
    ) -> Union[SkillModelInDB, None]:
        """Adding a new skill to the database

        Args:
            data (SkillCreateDataModel): New skill model

        Returns:
            Union[SkillModelInDB, None]: The model of the skill added to the database otherwise None
        """
        pass

    @abstractmethod
    async def get_skill_all(
        self, limit: int = 1000, last_skill_key: str = None
    ) -> ResponseItems[SkillModelInDB]:
        """Get all skills in the database

        Args:
            limit (int, optional): Limit of skills received. Defaults to 1000.
            last_user_key (str, optional): The last skill key received in the previous request. Defaults to None.

        Returns:
            ResponseItems[SkillModelInDB]: Query result
        """
        pass

    @abstractmethod
    async def get_skill_by_key(self, key: str) -> Union[SkillModelInDB, None]:
        """Get a skill by key from the database

        Args:
            key (str): The skill key in the database

        Returns:
            Union[SkillModelInDB, None]: If a skill is found, then returns SkillModelInDB otherwise None"""
        pass

    # Event
    @abstractmethod
    async def create_event(self, event: EventModelInDB) -> Union[EventModelInDB, None]:
        """Adding a new event to the database

        Args:
            event (EventModelInDB): New event model

        Returns:
            Union[EventModelInDB, None]: The model of the event added to the database otherwise None
        """
        pass

    @abstractmethod
    async def get_events_by_query(
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
        pass

    @abstractmethod
    async def get_all_events(
        self, limit: int = 1000, last_event_key: str = None
    ) -> ResponseItems[EventModelInDB]:
        """Get all events from the database

        Args:
            limit (int, optional): Limit of events received. Defaults to 1000.
            last_event_key (str, optional): The last event key received in the previous request.
            Defaults to None.

        Returns:
            ResponseItems[EventModelInDB]: Query result
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
    async def get_event_by_key(self, key: str) -> Union[EventModelInDB, None]:
        """Get a event by key from the database

        Args:
            key (str): The event key in the database

        Returns:
            Union[EventModelInDB, None]: If a event is found, then returns EventModelInDB otherwise None
        """
        pass

    @abstractmethod
    async def update_event_by_key(self, event: EventModelInput, key: str) -> None:
        """Updating of event data

        Args:
            event (EventModelInput): event data
            key (str): The event key in the database

        Raises:
            UpdateEventException: If the event data update was not successful

        Returns:
            None: Returns nothing
        """
        pass
