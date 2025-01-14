import hashlib
from datetime import datetime

from PIL import UnidentifiedImageError, Image
from PIL.ExifTags import TAGS

from app.models.file import File


class PhotoFileException(Exception):
    """
    Класс ошибок класса PhotoFile
    """
    pass


class PhotoFile(File):
    """
    Класс файла изображения
    """

    def __init__(self, filepath: str):
        """
        Метод инициализирующий класс
        :param filepath: (str) - Путь до файла
        """
        super().__init__(filepath)

        # Получение изображения
        try:
            self.__image = Image.open(filepath)
        except UnidentifiedImageError as ex:
            detail = "Передан не поддерживаемый файл для изображения"
            raise PhotoFileException(detail) from ex

        # Получение даты создания изображения
        self.__created_at = self.__get_created_at()
        # Получение хеш-суммы изображения
        self.__hash_sum = self.__get_hash_sum()

        # Чистка памяти
        del self.__image
        return

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def hash_sum(self) -> str:
        return self.__hash_sum

    def __get_created_at(self) -> datetime:
        """
        Метод возвращает дату создания изображения
        :return: (datetime)
        """
        # Получение метаданных изображения
        exif_data = self.__image.getexif()
        metadata = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}

        # Получение даты создания изображения
        created_at = datetime.strptime(metadata["DateTime"], '%Y:%m:%d %H:%M:%S') if metadata.get("DateTime") else None
        if not created_at:
            return self.__created_at

        return created_at

    def __get_hash_sum(self) -> str:
        """
        Метод возвращает хеш-сумму изображения
        :return: (str)
        """
        # Получение хеш-суммы изображения
        image_data = self.__image.tobytes()
        hash_sum = hashlib.sha256(image_data).hexdigest()

        return hash_sum
