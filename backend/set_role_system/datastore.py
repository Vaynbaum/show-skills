from db.models.role_model import RoleModel

SUPER_ADMIN = "super_admin"
ADMIN = "admin"
USER = "user"

roles: list[(RoleModel)] = [
    {"name_ru": "супер-администратор", "name_en": SUPER_ADMIN},
    {"name_ru": "администратор", "name_en": ADMIN},
    {"name_ru": "пользователь", "name_en": USER}]


