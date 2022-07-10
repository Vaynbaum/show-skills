import os
import io
from typing import BinaryIO, Union
from deta import Deta
from dotenv import load_dotenv
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image


from drive.abstract_drive_handler import AbstractDriveHandler
from exceptions.get_file_exception import GetFileException
from exceptions.get_photo_exception import GetPhotoException
from exceptions.upload_file_exception import UploadFileException
from exceptions.upload_photo_exception import UploadPhotoException


class DriveHandler(AbstractDriveHandler):
    def __init__(self):
        load_dotenv()
        self.__deta = Deta(os.getenv("DETA_PROJECT_KEY"))

    def __upload_file(
        self, name_file: str, name_drive: str, file: Union[BinaryIO, bytes]
    ):
        items = self.__deta.Drive(name_drive)
        try:
            return items.put(name_file, file)
        except Exception as e:
            print(e)
            raise UploadFileException(f"{e}")

    def __get_file(self, name_file: str, name_drive: str):
        items = self.__deta.Drive(name_drive)
        try:
            return items.get(name_file)
        except Exception as e:
            print(e)
            raise GetFileException(f"{e}")

    def __get_extension(self, name_file: str) -> str:
        extension_file = name_file.split(".")[-1]
        return extension_file

    def __resize_file(
        self, file: BinaryIO, extension_file: str, size_height: int, size_width: int
    ) -> bytes:
        img = Image.open(file)
        resized_img = img.resize((size_width, size_height), Image.ANTIALIAS)
        img_byte_arr = io.BytesIO()
        resized_img.save(img_byte_arr, format=extension_file)
        return img_byte_arr.getvalue()

    def join_file_name(self, file: UploadFile, name_file: str) -> str:
        extension_file = self.__get_extension(file.filename)
        return f"{name_file}.{extension_file}"

    

    def upload_photo(
        self,
        name_file: str,
        name_directory: str,
        file: UploadFile,
        size_height: int = None,
        size_width: int = None,
    ) -> str:
        if file.content_type.find("image") != -1:
            if (size_height is not None) and (size_width is not None):
                extension_file = self.__get_extension(file.filename)
                img = self.__resize_file(
                    file.file, extension_file, size_height, size_width
                )
            else:
                img = file.file

            try:
                return self.__upload_file(f"{name_directory}/{name_file}", "photos", img)
            except UploadFileException as e:
                print(e)
                raise UploadPhotoException(f"{e}")
        else:
            raise UploadPhotoException("Invalid file format")

    def get_photo(self, name_directory: str, name_file: str):
        extension_file = self.__get_extension(name_file)
        try:
            result = self.__get_file(f"{name_directory}/{name_file}", "photos")
            return (
                StreamingResponse(
                    result.iter_chunks(1024), media_type=f"image/{extension_file}"
                )
                if result is not None
                else None
            )
        except GetFileException as e:
            print(e)
            raise GetPhotoException(f"{e}")
