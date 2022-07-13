from typing import Union
from fastapi import HTTPException

from controllers.user_controller import UserController
from consts.name_roles import USER
from db.database_handler import DatabaseHandler
from models.response_items import ResponseItems
from models.result_subscribe_model import ResultSubscriptionModel
from models.user_model import ShortUserModelResponse, UserModelResponse
from models.subscription_model import SubscriptionModel


class SubscriptionController:
    def __init__(self, database_controller: DatabaseHandler):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)

    async def subscribe(self, username: str, token: str) -> ResultSubscriptionModel:
        """Subscribing to another user

        Args:
            username (str)
            token (str): access token

        Raises:
            HTTPException: If there is an attempt to subscribe to yourself
            or not a user or a subscription already exists
            HTTPException: If the favorite is not found or it failed to subscribe

        Returns:
            ResultSubscriptionModel: favorite and follower
        """
        follower = await self.__user_controller.get_user_by_token(token)
        if follower.username == username:
            raise HTTPException(
                status_code=400, detail="You can't subscribe to yourself"
            )

        result = list(
            filter(
                lambda item: username in item.favorite.username,
                follower.subscriptions,
            )
        )
        if len(result) != 0:
            raise HTTPException(status_code=400, detail="Subscription already exists")

        favorite = await self.__database_controller.get_user_by_username(username)
        if favorite is None:
            raise HTTPException(status_code=404, detail="Favorite not found")

        if (follower.role.name_en != USER) or (favorite.role.name_en != USER):
            raise HTTPException(status_code=400, detail="Some of you are non-users")

        subs = SubscriptionModel(favorite=favorite)
        favorite.followers.append(ShortUserModelResponse(**follower.dict()))
        follower.subscriptions.append(subs)
        users = [favorite.dict(), follower.dict()]
        result = await self.__database_controller.put_many_users(users)
        if "failed" in result:
            raise HTTPException(status_code=400, detail="Subscription failed")

        items_result = result["processed"]["items"]
        result = ResultSubscriptionModel(
            favorite=UserModelResponse(**items_result[0]),
            follower=UserModelResponse(**items_result[1]),
        )
        return result

    async def annul(self, username: str, token: str) -> ResultSubscriptionModel:
        """Cancel subscription

        Args:
            username (str)
            token (str): access token

        Raises:
            HTTPException: If the favorite is not found or unsubscribe failed

        Returns:
            ResultSubscriptionModel: favorite and follower
        """
        follower = await self.__user_controller.get_user_by_token(token)
        res = list(
            filter(
                lambda item: username in item.favorite.username, follower.subscriptions
            )
        )
        if len(res) == 0:
            raise HTTPException(status_code=404, detail="Favorite not found")

        follower.subscriptions.remove(res[0])
        favorite = await self.__database_controller.get_user_by_username(username)
        favorite.followers.remove(
            list(
                filter(
                    lambda item: follower.username in item.username,
                    favorite.followers,
                )
            )[0]
        )
        users = [favorite.dict(), follower.dict()]
        result = await self.__database_controller.put_many_users(users)
        if "failed" in result:
            raise HTTPException(status_code=400, detail="Unsubscribe failed")
        items_result = result["processed"]["items"]
        result = ResultSubscriptionModel(
            favorite=UserModelResponse(**items_result[0]),
            follower=UserModelResponse(**items_result[1]),
        )
        return result

    async def get_subscriptions(
        self, token: str, limit: Union[int, None]
    ) -> ResponseItems[SubscriptionModel]:
        """Getting all of my subscriptions

        Args:
            token (str): access token
            limit (Union[int, None]): Limit of subscriptions received

        Returns:
            ResponseItems[SubscriptionModel]: Query result
        """        
        user = await self.__user_controller.get_user_by_token(token)

        if limit is None:
            return user.subscriptions
        else:
            return user.subscriptions[:limit]
