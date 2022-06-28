from fastapi import APIRouter
from controllers.auth_controller import AuthController
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.schemas.user_schema import AuthSchema, SignupSchema

auth_controller = AuthController()
security = HTTPBearer()
router = APIRouter(tags=['Auth'])


@router.post("/signup")
def signup(user_details: SignupSchema):
    return auth_controller.signup(user_details)


@router.post('/login')
def login(user_details: AuthSchema):
    return auth_controller.login(user_details)


@router.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    return auth_controller.refresh_token(credentials)
