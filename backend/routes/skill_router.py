from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security


from controllers.skill_controller import SkillController
from db.database_handler import DatabaseHandler
from depends.get_db import get_db
from depends.get_drive import get_drive
from handlers.access.role_access import RoleAccess
from models.http_error import HTTPError
from models.response_items import ResponseItems
from models.skill_model import SkillCreateDataModel, SkillInDBModel
from handlers.drive_handler import DriveHandler
from handlers.access_handler import AccessHandler
from consts.name_roles import ADMIN, SUPER_ADMIN, USER

security = HTTPBearer()
router = APIRouter(tags=["Skill"])


@router.post(
    "/create",
    responses={
        200: {"model": SkillInDBModel},
        400: {
            "model": HTTPError,
            "description": "If the user key is invalid or the skill failed to add",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Adding a new skill to the database",
)
async def create(
    skill: SkillCreateDataModel,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(SUPER_ADMIN), RoleAccess(ADMIN)],
    )
    async def inside_func(skill):
        skill_controller = SkillController(db, drive)
        return await skill_controller.create_skill(skill)

    return await inside_func(skill)


@router.post(
    "/upload_icon/",
    responses={
        200: {"model": str},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, the image format 
            is invalid or the upload failed""",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Uploading the skill icon to disk",
)
async def upload_icon_skill(
    file: UploadFile,
    name: str = Query(example="Python"),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(SUPER_ADMIN), RoleAccess(ADMIN)],
    )
    async def inside_func(name, file):
        skill_controller = SkillController(db, drive)
        return skill_controller.upload_icon_skill(name, file)

    return await inside_func(name, file)


@router.get(
    "/icon/{name_file}",
    responses={
        200: {"description": "File in the format *StreamingResponse*"},
        400: {
            "model": HTTPError,
            "description": "if the file could not be retrieved",
        },
    },
    summary="Getting the skill icon by the name of the photo",
)
async def get_icon_by_name_file(
    name_file: str = Path(example="python.png"),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    skill_controller = SkillController(db, drive)
    return skill_controller.get_icon_by_name_file(name_file)


@router.get(
    "/all",
    responses={200: {"model": ResponseItems[SkillInDBModel]}},
    summary="Getting all skills from the database",
)
async def get_all_skills(
    limit: int = Query(default=100),
    last_skill_key: str = Query(default=None),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    skill_controller = SkillController(db, drive)

    return await skill_controller.get_skill_all(limit, last_skill_key)


@router.post(
    "/add/to_myself",
    responses={
        200: {"model": SkillInDBModel},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid, skill alreade exists or 
            failed to add skill""",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        404: {
            "model": HTTPError,
            "description": "Skill is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Add a skill to yourself",
)
async def add_skill_to_myself(
    skill_key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(USER)],
    )
    async def inside_func(skill_key, token):
        skill_controller = SkillController(db, drive)
        return await skill_controller.add_skill(skill_key, token)

    return await inside_func(skill_key, credentials.credentials)


@router.delete(
    "/remove/at_yorself",
    responses={
        200: {"model": List[SkillInDBModel]},
        400: {
            "model": HTTPError,
            "description": """If the user key is invalid or failed to add skill""",
        },
        401: {
            "model": HTTPError,
            "description": "If the token is invalid, expired or scope is invalid",
        },
        403: {
            "model": HTTPError,
            "description": """If authentication failed, invalid authentication credentials 
            or no access rights to this method""",
        },
        404: {
            "model": HTTPError,
            "description": "Skill is not found",
        },
        500: {
            "model": HTTPError,
            "description": "If an error occurred while verifying access",
        },
    },
    summary="Delete a skill from yourself",
)
async def delete_skill_to_myself(
    skill_key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
    drive: DriveHandler = Depends(get_drive),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [RoleAccess(USER)],
    )
    async def inside_func(skill_key, token):
        skill_controller = SkillController(db, drive)
        return await skill_controller.remove_skill(skill_key, token)

    return await inside_func(skill_key, credentials.credentials)
