import os
import io
from deta import Deta
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

from drive.abstract_drive_handler import AbstractDriveHandler


class DriveHandler(AbstractDriveHandler):
    def __init__(self):
        load_dotenv()
        self.__deta = Deta(os.getenv("DETA_PROJECT_KEY"))

    def __upload_file(self, name_file: str, name_drive: str, file):
        items = self.__deta.Drive(name_drive)
        result = items.put(name_file, file)
        return result

    def __get_file(self, name_file, name_drive):
        items = self.__deta.Drive(name_drive)
        return items.get(name_file)

    def __get_extension(self, name_file):
        extension_file = name_file.split(".")[-1]
        return extension_file

    def __resize_file(self, file, extension_file, size_height, size_width):
        img = Image.open(file)
        resized_img = img.resize((size_width, size_height), Image.ANTIALIAS)
        img_byte_arr = io.BytesIO()
        resized_img.save(img_byte_arr, format=extension_file)
        return img_byte_arr.getvalue()

    def upload_photo(
        self,
        name_file: str,
        name_directory: str,
        file: UploadFile,
        size_height: int,
        size_width: int,
    ) -> str:
        if file.content_type.find("image") != -1:
            extension_file = self.__get_extension(file.filename)
            img = self.__resize_file(file.file, extension_file, size_height, size_width)
            name_file = f"{name_file}.{extension_file}"
            self.__upload_file(f"{name_directory}/{name_file}", "photos", img)
            return name_file
        raise HTTPException(status_code=402, detail="Invalid file format")

    def get_photo(self, name_directory: str, name_file: str):
        extension_file = self.__get_extension(name_file)
        result = self.__get_file(f"{name_directory}/{name_file}", "photos")
        return (
            StreamingResponse(
                result.iter_chunks(1024), media_type=f"image/{extension_file}"
            )
            if result is not None
            else None
        )
