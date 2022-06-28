from fastapi import APIRouter
from controllers.user_controller import UserController
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.schemas.user_schema import UserResponse

auth_controller = UserController()
security = HTTPBearer()

router = APIRouter(tags=['User'])


@router.post("/{email}")
def get_by_email(email: str, credentials: HTTPAuthorizationCredentials = Security(security)):
    return auth_controller.get_user_by_email(email, credentials)
