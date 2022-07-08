from fastapi import HTTPException
from controllers.user_controller import UserController
from db.abstract_database_handler import AbstractDatabaseHandler
from models.message_model import MessageModel
from models.role_model import RoleModelResponse


class RoleController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
    ):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)

    async def get_all_roles(self):
        return await self.__database_controller.get_role_all_can_assign()

    async def assign_role_to_user(self, role_key, user_key):
        role = await self.__database_controller.get_role_by_key(role_key)
        if role is None:
            raise HTTPException(status_code=400, detail="Role not found")
        
        await self.__database_controller.simple_data_update_to_user(
            {"role": (RoleModelResponse(**role.dict())).dict(), "role_key": role.key},
            user_key,
        )
        return MessageModel(message="Role successfully assigned")
