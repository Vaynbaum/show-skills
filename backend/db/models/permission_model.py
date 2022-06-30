from pydantic import BaseModel

from db.models.role_model import RoleModel

# TypeAttribute = TypeVar('TypeAttribute')


# class PermissionModel(BaseModel):
#     key: str | None
#     action: int
#     object: int
#     type_object: int
#     roles: List[TypeVar('RoleModel', bound=RoleModel)]
#     attributes: Optional[Dict[str, int]]