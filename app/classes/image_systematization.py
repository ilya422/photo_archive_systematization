import logging
import os.path

from app.models import PhotoFile, PhotoFileException, FileException


class ImageSystematizationException(Exception):
    """
    Класс ошибок ImageSystematization
    """
    pass

class ImageSystematization:
    """
        Класс систематизации изображений
    """

    @classmethod
    def __get_photo_files_info(cls, source_dir: str) -> list[PhotoFile]:
        """
        Метод возвращает список исходных изображений
        :param source_dir: (str) - Путь до каталога источника изображений
        :return: (list[PhotoFile])
        """
        photo_info = {}
        for root, _, files in os.walk(source_dir):
            for file in files:
                # Получение объекта файла изображения
                filepath = os.path.join(root, file)
                try:
                    photo_file = PhotoFile(filepath=filepath)
                except (FileException, PhotoFileException) as ex:
                    logging.error(f"Не удалось обработать файл: {filepath}. [{ex}]")
                    continue

                # Поиск исходного изображения (чистка дублей)
                if not photo_info.get(photo_file.hash_sum):
                    photo_info[photo_file.hash_sum] = photo_file
                    continue
                if photo_file.created_at < photo_info[photo_file.hash_sum].created_at:
                    photo_info[photo_file.hash_sum] = photo_file
                    continue

        return list(photo_info.values())

    @classmethod
    def run(cls, source_dir: str, result_dir: str) -> None:
        """
        Метод для запуска систематизации изображений
        :param source_dir: (str) - Путь до каталога источника изображений
        :param result_dir: (str) - Путь до каталога результирующих изображений
        :return: (None)
        """
        # Проверка параметров
        if not isinstance(source_dir, str):
            detail = f"Путь до каталога источника изображений не является строкой"
            raise ImageSystematizationException(detail)
        if not isinstance(result_dir, str):
            detail = f"Путь до каталога источника изображений не является строкой"
            raise ImageSystematizationException(detail)
        if not os.path.exists(source_dir):
            detail = f"Не найдена папка источника изображений: {source_dir}"
            raise ImageSystematizationException(detail)

        # Получение исходных изображений
        photos = cls.__get_photo_files_info(source_dir=source_dir)

        # Распределение изображений
        for photo in photos:
            # Создаём подкаталог для года создания изображения
            dir_path = os.path.join(result_dir, str(photo.created_at.year))
            os.makedirs(dir_path, exist_ok=True)

            # Копируем исходное изображение в подкаталог
            new_filepath = f"{dir_path}\\{photo.filename}"
            try:
                photo.copy_file(new_filepath)
            except FileException as ex:
                logging.error(f"Не удалось скопировать файл: {photo.filepath}. [{ex}]")
                raise ImageSystematizationException from ex

        return