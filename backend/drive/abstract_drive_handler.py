from abc import ABC, abstractmethod
from typing import Union
from fastapi.responses import StreamingResponse
from fastapi import UploadFile


class AbstractDriveHandler(ABC):
    @abstractmethod
    def upload_photo(
        self,
        name_file: str,
        name_directory: str,
        file: UploadFile,
        size_height: int = None,
        size_width: int = None,
    ) -> str:
        """Загружает фотографию на диск"""
        pass

    @abstractmethod
    def get_photo(
        self, name_directory: str, name_file: str
    ) -> Union[StreamingResponse, None]:
        """Получение фотографии по имени и директории"""
        pass

    @abstractmethod
    def join_file_name(self, file: UploadFile, name_file: str) -> str:
        pass

