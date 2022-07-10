from typing import Union
from deta import Deta

from exceptions.update_item_exception import UpdateItemException
from models.response_items import ResponseItems
from models.user_model import UserInDBModel, UserModelResponse


class UserDatabaseHandler:
    def __init__(self, deta: Deta):
        self.__users_db = deta.AsyncBase("users")

    async def get_one_by_query(self, query: dict = None) -> Union[UserInDBModel, None]:
        """Get one user by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.

        Returns:
            Union[UserInDBModel, None]: If a user is found, then returns UserInDBModel otherwise None
        """
        res_fetch = await self.__users_db.fetch(query, limit=1)
        if res_fetch.count > 0:
            user_dict = res_fetch.items[0]
            return UserInDBModel(**user_dict)
        else:
            return None

    async def get_many_by_query(
        self, query: dict = None, limit: int = 1000, last_user_key: str = None
    ) -> ResponseItems[UserModelResponse]:
        """Get users by different criteria from the database

        Args:
            query (dict, optional): Choosing criteria. Defaults to None.
            limit (int, optional): Limit of users received. Defaults to 1000.
            last_user_key (str, optional): The last user key received in the previous request. Defaults to None.

        Returns:
            ResponseItems[UserModelResponse]: Query result
        """
        print(query, limit, last_user_key)
        result = await self.__users_db.fetch(query, limit=limit, last=last_user_key)
        return ResponseItems[UserModelResponse](
            count=result.count, last=result.last, items=result.items
        )

    async def create(self, user: UserInDBModel) -> Union[UserInDBModel, None]:
        """Adding a new user to the database

        Args:
            user (UserInDBModel): New user model

        Returns:
            Union[UserInDBModel, None]: The model of the user added to the database otherwise None
        """
        try:
            user = await self.__users_db.put(user.dict())
            return UserInDBModel(**user)
        except:
            return None

    async def get_by_key(self, key: str) -> Union[UserInDBModel, None]:
        """Get a user by key from the database

        Args:
            key (str): The user's key in the database

        Returns:
            Union[UserInDBModel, None]: If a user is found, then returns UserInDBModel otherwise None
        """
        user = await self.__users_db.get(key)
        return UserInDBModel(**user) if user is not None else None

    async def delete_by_key(self, key: str) -> None:
        """Delete a user from the database by key

        Args:
            key (str): The user's key in the database

        Returns:
            None: Returns nothing
        """
        return await self.__users_db.delete(key)

    async def put_many(self, users: list) -> dict:
        """Put multiple users in the database

        Args:
            users (list): List of users

        Returns:
            dict: Returns a dict with "processed" and "failed"(if any) items
        """
        return await self.__users_db.put_many(users)

    async def append_links(self, links: list, key: str) -> None:
        """Add links to the user

        Args:
            links (list): List of links
            key (str): The user's key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__users_db.update(
                {"links": self.__users_db.util.append(links)}, key
            )
        except BaseException as e:
            print(e)
            raise UpdateItemException("Updating data was not successful")

    async def append_skills(self, skills: list, key: str) -> None:
        """Add skills to the user

        Args:
            skills (list): List of skills
            key (str): The user's key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        print(skills)
        try:
            return await self.__users_db.update(
                {"skills": self.__users_db.util.append(skills)}, key
            )
        except BaseException as e:
            print(e)
            raise UpdateItemException("Updating data was not successful")

    async def simple_data_update(self, data: dict, key: str) -> None:
        """Simple updating of user data

        Args:
            data (dict): user data
            key (str): The user's key in the database

        Raises:
            UpdateItemException: If data update was not successful

        Returns:
            None: Returns nothing
        """
        try:
            return await self.__users_db.update(data, key)
        except BaseException as e:
            print(e)
            raise UpdateItemException("Updating data was not successful")
