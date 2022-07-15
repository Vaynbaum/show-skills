import os
import json
from dotenv import load_dotenv
from deta import Deta


def main():
    load_dotenv()
    deta = Deta(os.getenv("DETA_PROJECT_KEY"))
    roles_base = deta.Base("roles")
    if (roles_base.fetch()).count == 0:
        with open("files/role.json", "r", encoding="utf-8") as f:
            content = json.load(f)
            roles_base.put_many(content)


if __name__ == "__main__":
    main()
