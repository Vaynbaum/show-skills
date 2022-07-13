from fastapi import HTTPException

from controllers.user_controller import UserController
from db.database_handler import DatabaseHandler
from exceptions.update_suggestion_exception import UpdateSuggestionException
from models.message_model import MessageModel
from models.response_items import ResponseItems
from models.short_user_model_response import ShortUserModelResponse
from models.suggestion_model import (
    SuggestionInDBModel,
    SuggestionInputModel,
    SuggestionTickModel,
)


class SuggestionController:
    def __init__(self, database_controller: DatabaseHandler):
        self.__database_controller = database_controller
        self.__user_controller = UserController(database_controller)

    async def add_suggestion(
        self, suggestion: SuggestionInputModel, token: str
    ) -> SuggestionInDBModel:
        """Send an suggestion

        Args:
            suggestion (SuggestionInputModel)
            token (str): access token

        Raises:
            HTTPException: If the suggestion is not sent

        Returns:
            SuggestionInDBModel
        """        
        user = await self.__user_controller.get_user_by_token(token)
        suggestion = SuggestionInDBModel(
            **suggestion.dict(),
            completed=False,
            readed=False,
            sender=ShortUserModelResponse(**user.dict()),
        )

        result = await self.__database_controller.add_suggestion(suggestion)
        if result is None:
            raise HTTPException(status_code=400, detail="Suggestion unsent")
        return result

    async def get_all_suggestions(
        self, readed: bool, completed: bool, limit: int, last_key: str
    ) -> ResponseItems[SuggestionInDBModel]:
        """_summary_

        Args:
            readed (bool): The suggestion is read
            completed (bool): The suggestion is complet
            limit (int): Limit of suggestions received
            last_key (str): The last suggestion key received in the previous request

        Returns:
            ResponseItems[SuggestionInDBModel]: Query result
        """        
        return await self.__database_controller.get_all_suggestions(
            {"readed": readed, "completed": completed}, limit, last_key
        )

    async def tick_suggestion(
        self, suggestion: SuggestionTickModel, suggestion_key: str
    ) -> MessageModel:
        """Mark the status of the suggestion

        Args:
            suggestion (SuggestionTickModel)
            suggestion_key (str)

        Raises:
            HTTPException: If the suggestion data update was not successful

        Returns:
            MessageModel
        """        
        try:
            await self.__database_controller.update_suggestion(
                suggestion.dict(), suggestion_key
            )
            return MessageModel(message="Ticking  successful")
        except UpdateSuggestionException as e:
            
            raise HTTPException(status_code=400, detail=f"{e}")
