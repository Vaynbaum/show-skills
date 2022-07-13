from fastapi import APIRouter
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from controllers.auth_controller import AuthController
from db.database_handler import DatabaseHandler
from models.http_error import HTTPError
from models.message_model import MessageModel
from models.token_model import AccessTokenModel, PairTokenModel
from models.user_model import AuthModel, SignupModel

database_handler = DatabaseHandler()
auth_controller = AuthController(database_handler)
security = HTTPBearer()
router = APIRouter(tags=["Auth"])


@router.post(
    "/signup",
    responses={
        200: {"model": MessageModel},
        401: {
            "model": HTTPError,
            "description": "If the email or password is already taken or failed to register",
        },
    },
    summary="Register in the system",
)
async def signup(user_details: SignupModel):
    return await auth_controller.signup(user_details)


@router.post(
    "/login",
    responses={
        200: {"model": PairTokenModel},
        401: {
            "model": HTTPError,
            "description": "If the password or login is invalid",
        },
    },
    summary="Log in to the system",
)
async def login(user_details: AuthModel):
    return await auth_controller.login(user_details)


@router.get(
    "/refresh_token",
    responses={
        200: {"model": AccessTokenModel},
        401: {
            "model": HTTPError,
            "description": "If the refresh token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": "If not authenticated or invalid authentication credentials",
        },
    },
    summary="Create a new access token by refresh token",
)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    return auth_controller.refresh_token(credentials)
