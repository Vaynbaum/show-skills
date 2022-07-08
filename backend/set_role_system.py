import os
from dotenv import load_dotenv
from deta import Deta

from consts.name_roles import SUPER_ADMIN, USER, ADMIN


def main():
    load_dotenv()
    deta = Deta(os.getenv("DETA_PROJECT_KEY"))
    roles_base = deta.Base("roles")

    if (roles_base.fetch()).count == 0:
        roles_base.put_many(
            [
                {
                    "name_ru": "супер-администратор",
                    "name_en": SUPER_ADMIN,
                    "can_assign": False,
                },
                {"name_ru": "администратор", "name_en": ADMIN, "can_assign": True},
                {"name_ru": "пользователь", "name_en": USER, "can_assign": True},
            ]
        )


if __name__ == "__main__":
    main()
