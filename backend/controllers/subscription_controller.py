from fastapi import HTTPException
from controllers.user_controller import UserController
from consts.name_roles import USER


from db.abstract_database_handler import AbstractDatabaseHandler
from models.user_model import ShortResponseUserModel
from models.subscription_model import SubscriptionModel
from models.message_model import MessageModel


class SubscriptionController:
    def __init__(self, database_controller: AbstractDatabaseHandler):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)

    async def subscribe(self, username, token: str):
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
            raise HTTPException(status_code=400, detail="Favorite not found")

        if (follower.role.name_en != USER) or (favorite.role.name_en != USER):
            raise HTTPException(status_code=400, detail="Some of you are non-users")

        if favorite != None:
            subs = SubscriptionModel(favorite=favorite)
            favorite.followers.append(ShortResponseUserModel(**follower.dict()))
            follower.subscriptions.append(subs)
            users = [favorite.dict(), follower.dict()]
            result = await self.__database_controller.put_many_users(users)
            if "failed" == result:
                raise HTTPException(status_code=400, detail="Subscription failed")
            else:
                return MessageModel(message="Subscription successful")
        else:
            raise HTTPException(status_code=400, detail="Favorite not found")

    async def annul(self, username, token: str):
        follower = await self.__user_controller.get_user_by_token(token)
        res = list(
            filter(
                lambda item: username in item.favorite.username, follower.subscriptions
            )
        )
        if len(res) == 0:
            raise HTTPException(status_code=400, detail="Favorite not found")
        else:
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
            if "failed" == result:
                raise HTTPException(status_code=400, detail="Unsubscribe failed")
            else:
                return MessageModel(message="Unsubscribe successful")
