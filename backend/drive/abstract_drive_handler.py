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
        size_height: int,
        size_width: int,
    ) -> str:
        """Загружает фотографию на диск"""
        pass

    @abstractmethod
    def get_photo(
        self, name_directory: str, name_file: str
    ) -> Union[StreamingResponse, None]:
        """Получение фотографии по имени и директории"""
        pass
