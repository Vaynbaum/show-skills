from typing import Union
from fastapi import APIRouter, Query, UploadFile, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from controllers.skill_controller import SkillController
from db.abstract_database_handler import AbstractDatabaseHandler
from db.database_handler import DatabaseHandler
from models.response_items import ResponseItems
from models.skill_model import SkillCreateDataModel, SkillInDBModel
from drive.abstract_drive_handler import AbstractDriveHandler
from drive.drive_handler import DriveHandler
from handlers.access_handler import AccessHandler, RoleAccessModel
from consts.name_roles import ADMIN, SUPER_ADMIN, USER


database_handler: AbstractDatabaseHandler = DatabaseHandler()
drive_handler: AbstractDriveHandler = DriveHandler()
skill_controller = SkillController(database_handler, drive_handler)
security = HTTPBearer()
access_handler = AccessHandler(database_handler)

router = APIRouter(tags=["Skill"])


@router.post("/create")
async def create(
    skill: SkillCreateDataModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=SUPER_ADMIN), RoleAccessModel(name=ADMIN)],
    )
    async def inside_func(skill):
        return await skill_controller.create_skill(skill)

    return await inside_func(skill)


@router.post("/upload_icon/", responses={200: {"model": str}})
async def upload_icon_skill(
    file: UploadFile,
    name: str = Query(example="Python"),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=SUPER_ADMIN), RoleAccessModel(name=ADMIN)],
    )
    async def inside_func(name, file):
        return skill_controller.upload_icon_skill(name, file)

    return await inside_func(name, file)


@router.get("/icon/{name_file}")
async def get_icon_by_name_file(name_file: str = Path(example="python.png")):
    return skill_controller.get_icon_by_name_file(name_file)


@router.get("/all", responses={200: {"model": ResponseItems[SkillInDBModel]}})
async def get_all_skills(limit: int = 100, last_user_key: str = None):
    return await skill_controller.get_skill_all(limit, last_user_key)


@router.post("/add/to_myself")
async def add_skill_to_myself(
    skill_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=USER)],
    )
    async def inside_func(skill_key, token):
        return await skill_controller.add_skill(skill_key, token)

    return await inside_func(skill_key, credentials.credentials)


@router.delete("/remove/at_yorself")
async def add_skill_to_myself(
    skill_key: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccessModel(name=USER)],
    )
    async def inside_func(skill_key, token):
        return await skill_controller.remove_skill(skill_key, token)

    return await inside_func(skill_key, credentials.credentials)
