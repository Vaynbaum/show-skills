import os
import io
from typing import BinaryIO, Union
from deta import Deta
from deta.drive import DriveStreamingBody
from dotenv import load_dotenv
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

from exceptions.get_file_exception import GetFileException
from exceptions.get_photo_exception import GetPhotoException
from exceptions.upload_file_exception import UploadFileException
from exceptions.upload_photo_exception import UploadPhotoException


class DriveHandler:
    def __init__(self, deta: Deta):
        load_dotenv()
        self.__deta = deta

    def __upload_file(
        self, name_file: str, name_drive: str, file: Union[BinaryIO, bytes]
    ) -> str:
        """Uploading files

        Args:
            name_file (str)
            name_drive (str): Name of the folder for files
            file (Union[BinaryIO, bytes])

        Raises:
            UploadFileException: If the file could not be uploaded

        Returns:
            str: The name of the directory with the file name
        """
        items = self.__deta.Drive(name_drive)
        try:
            return items.put(name_file, file)
        except Exception as e:

            raise UploadFileException(f"{e}")

    def __get_file(
        self, name_file: str, name_drive: str
    ) -> Union[DriveStreamingBody, None]:
        """Getting a file

        Args:
            name_file (str)
            name_drive (str): Name of the folder for files

        Raises:
            GetFileException: If the file could not be retrieved

        Returns:
            Union[DriveStreamingBody, None]: The resulting image
        """
        items = self.__deta.Drive(name_drive)
        try:
            return items.get(name_file)
        except Exception as e:

            raise GetFileException(f"{e}")

    def __get_extension(self, name_file: str) -> str:
        """Getting the file extension

        Args:
            name_file (str)

        Returns:
            str: file extension
        """
        extension_file = name_file.split(".")[-1]
        return extension_file

    def __resize_file(
        self, file: BinaryIO, extension_file: str, size_height: int, size_width: int
    ) -> bytes:
        """Changing the file size

        Args:
            file (BinaryIO)
            extension_file (str)
            size_height (int)
            size_width (int)

        Returns:
            bytes: The resulting image
        """
        img = Image.open(file)
        resized_img = img.resize((size_width, size_height), Image.ANTIALIAS)
        img_byte_arr = io.BytesIO()
        resized_img.save(img_byte_arr, format=extension_file)
        return img_byte_arr.getvalue()

    def join_file_name(self, file: UploadFile, name_file: str) -> str:
        """Combining the file name with the extension

        Args:
            file (UploadFile)
            name_file (str): Initial file name

        Returns:
            str: Received name
        """
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
        """Uploading an image to disk

        Args:
            name_file (str)
            name_directory (str)
            file (UploadFile)
            size_height (int, optional): Defaults to None.
            size_width (int, optional): Defaults to None.

        Raises:
            UploadPhotoException: If the image format is invalid or the upload failed

        Returns:
            str: The name of the directory and file
        """
        if file.content_type.find("image") == -1:
            raise UploadPhotoException("Invalid file format")

        if (size_height is not None) and (size_width is not None):
            extension_file = self.__get_extension(file.filename)
            img = self.__resize_file(file.file, extension_file, size_height, size_width)
        else:
            img = file.file

        try:
            return self.__upload_file(f"{name_directory}/{name_file}", "photos", img)
        except UploadFileException as e:

            raise UploadPhotoException(f"{e}")

    def get_photo(
        self, name_directory: str, name_file: str
    ) -> Union[StreamingResponse, None]:
        """Getting a photo by name and directory

        Args:
            name_directory (str)
            name_file (str)

        Raises:
            GetPhotoException: If the file could not be retrieved

        Returns:
            Union[StreamingResponse, None]: The resulting image
        """
        extension_file = self.__get_extension(name_file)
        try:
            result = self.__get_file(f"{name_directory}/{name_file}", "photos")
            return (
                StreamingResponse(
                    result.iter_chunks(), media_type=f"image/{extension_file}"
                )
                if result is not None
                else None
            )
        except GetFileException as e:

            raise GetPhotoException(f"{e}")
