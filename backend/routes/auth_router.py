from fastapi import APIRouter
from controllers.auth_controller import AuthController
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from db.models.user_model import AuthModel, SignupModel

database_handler: AbstractDatabaseHandler = DatabaseHandler()
auth_controller = AuthController(database_handler)
security = HTTPBearer()
router = APIRouter(tags=['Auth'])


@router.post("/signup")
def signup(user_details: SignupModel):
    return auth_controller.signup(user_details)


@router.post('/login')
def login(user_details: AuthModel):
    return auth_controller.login(user_details)


@router.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    return auth_controller.refresh_token(credentials)
