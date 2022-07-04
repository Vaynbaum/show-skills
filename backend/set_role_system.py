import os
from dotenv import load_dotenv
from deta import Deta

from datastore import roles

load_dotenv()
deta = Deta(os.getenv("DETA_PROJECT_KEY"))


def main():
    roles_base = deta.Base("roles")

    roles = roles_base.fetch()
    if roles.count == 0:
        roles_base.put_many(roles)


if __name__ == "__main__":
    main()
