from fastapi import HTTPException
from db.abstract_database_handler import AbstractDatabaseHandler
from exceptions.update_user_data_exception import UpdateUserDataException
from models.message_model import MessageModel
from models.role_model import RoleModelResponse


class RoleController:
    def __init__(
        self,
        database_controller: AbstractDatabaseHandler,
    ):
        self.__database_controller = database_controller

    async def get_all_roles(self):
        return await self.__database_controller.get_role_all_can_assign()

    async def assign_role_to_user(self, role_key: str, user_key: str):
        role = await self.__database_controller.get_role_by_key(role_key)
        if role is None:
            raise HTTPException(status_code=400, detail="Role not found")

        try:
            await self.__database_controller.update_simple_data_to_user(
                {
                    "role": (RoleModelResponse(**role.dict())).dict(),
                    "role_key": role.key,
                },
                user_key,
            )
        except UpdateUserDataException as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")
        return MessageModel(message="Role successfully assigned")
