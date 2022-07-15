from deta import Deta
import os
from dotenv import load_dotenv

from db.database_handler import DatabaseHandler


async def get_db():
    load_dotenv()
    deta = Deta(os.getenv("DETA_PROJECT_KEY"))
    return DatabaseHandler(deta)
