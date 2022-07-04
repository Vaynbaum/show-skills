from fastapi import APIRouter
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from controllers.auth_controller import AuthController
from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from models.message_model import MessageModel
from models.token_model import AccessTokenModel, PairTokenModel
from models.user_model import AuthModel, SignupModel

database_handler: AbstractDatabaseHandler = DatabaseHandler()
auth_controller = AuthController(database_handler)
security = HTTPBearer()
router = APIRouter(tags=["Auth"])


@router.post("/signup", responses={200: {"model": MessageModel}})
async def signup(user_details: SignupModel):
    return await auth_controller.signup(user_details)


@router.post("/login", responses={200: {"model": PairTokenModel}})
async def login(user_details: AuthModel):
    return await auth_controller.login(user_details)


@router.get("/refresh_token", responses={200: {"model": AccessTokenModel}})
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    return auth_controller.refresh_token(credentials)
