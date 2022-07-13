from fastapi import HTTPException
from db.database_handler import DatabaseHandler
from exceptions.update_user_data_exception import UpdateUserDataException
from models.message_model import MessageModel
from models.response_items import ResponseItems
from models.role_model import RoleInDBModel, RoleModelResponse


class RoleController:
    def __init__(
        self,
        database_controller: DatabaseHandler,
    ):
        self.__database_controller = database_controller

    async def get_all_roles(self) -> ResponseItems[RoleInDBModel]:
        """Getting all roles from the database

        Returns:
            ResponseItems[RoleInDBModel]: Query result
        """
        return await self.__database_controller.get_role_all_can_assign()

    async def assign_role_to_user(
        self, role_key: str, user_key: str
    ) -> RoleModelResponse:
        """Assign a role to a user

        Args:
            role_key (str)
            user_key (str)

        Raises:
            HTTPException: If the role is not found or
            the user data update was not successful

        Returns:
            RoleModelResponse
        """
        role = await self.__database_controller.get_role_by_key(role_key)
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found")

        role = RoleModelResponse(**role.dict())
        try:
            await self.__database_controller.update_simple_data_to_user(
                {
                    "role": role.dict(),
                    "role_key": role.key,
                },
                user_key,
            )
        except UpdateUserDataException as e:
            
            raise HTTPException(status_code=400, detail=f"{e}")
        return role
