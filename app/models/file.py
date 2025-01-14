import os
import shutil
from datetime import datetime

class FileException(Exception):
    """
    Класс ошибок класса File
    """
    pass


class File:
    """
    Класс файла
    """

    def __init__(self, filepath: str):
        """
        Метод инициализирующий класс
        :param filepath: (str) - Путь до файла
        """
        # Проверка параметров
        if not isinstance(filepath, str):
            detail = "Путь до файла должен быть строкой"
            raise FileException(detail)

        if not os.path.exists(filepath):
            detail = f"Не найден файл по переданному пути: {filepath}"
            raise FileException(detail)

        self.__filepath = filepath
        self.__filename = os.path.basename(filepath)
        self.__created_at = self.__get_created_at()

    @property
    def filepath(self) -> str:
        return self.__filepath

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    def __get_created_at(self) -> datetime:
        """
        Метод возвращает дату создания файла
        :return: (datetime)
        """
        # Получение даты создания изображения
        created_at = datetime.fromtimestamp(os.path.getctime(self.__filepath))
        return created_at

    def copy_file(self, path: str) -> None:
        """
        Метод копирует файл
        :param path: (str) - Путь копирования
        :return: (None)
        """
        # Проверка параметров
        if not isinstance(path, str):
            detail = "Путь копирования должен быть строкой"
            raise FileException(detail)

        base, extension = os.path.splitext(path)
        file_number = 1
        while os.path.exists(path):
            path = f"{base} ({file_number}){extension}"
            file_number += 1

        # Копируем изображение
        shutil.copy2(src=self.__filepath, dst=path)
        return