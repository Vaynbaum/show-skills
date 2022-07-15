from deta import Deta
import os
from dotenv import load_dotenv

from handlers.drive_handler import DriveHandler


async def get_drive():
    load_dotenv()
    deta = Deta(os.getenv("DETA_PROJECT_KEY"))
    return DriveHandler(deta)
