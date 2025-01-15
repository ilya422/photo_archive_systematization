import asyncio
import logging
import os.path

from tqdm import tqdm

from app.models import PhotoFile, PhotoFileException, FileException
from config.app import MAX_COUNT_ASYNC_TASK


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
        # Проверка параметров
        if not isinstance(source_dir, str):
            detail = f"Путь до каталога источника изображений не является строкой"
            raise ImageSystematizationException(detail)

        photo_info = {}
        for root, dirs, files in os.walk(source_dir):
            progress_bar = tqdm(desc=f'Обработка каталога: {root}', total=len(files))
            for file in files:
                # Получение объекта файла изображения
                filepath = os.path.join(root, file)
                try:
                    photo_file = PhotoFile(filepath=filepath)
                except (FileException, PhotoFileException) as ex:
                    logging.error(f"Не удалось обработать файл: {filepath}. [{ex}]")
                    continue
                progress_bar.update(1)
                # Поиск исходного изображения (чистка дублей)
                if not photo_info.get(photo_file.hash_sum):
                    photo_info[photo_file.hash_sum] = photo_file
                    continue
                if photo_file.created_at < photo_info[photo_file.hash_sum].created_at:
                    photo_info[photo_file.hash_sum] = photo_file
                    continue
            progress_bar.close()
        return list(photo_info.values())

    @classmethod
    async def run(cls, source_dir: str, result_dir: str) -> None:
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

        # Копирование изображений
        progress_bar = tqdm(desc=f'Копирование изображений', total=len(photos))
        step_len = MAX_COUNT_ASYNC_TASK
        exist_file_paths = set()
        for step_from in range(0, len(photos), step_len):
            tasks = []
            for photo in photos[step_from:step_from + step_len]:
                # Создание подкаталога для года создания изображения
                dir_path = os.path.join(result_dir, str(photo.created_at.year))
                os.makedirs(dir_path, exist_ok=True)

                # Формирование имени для нового файла
                new_filepath = f"{dir_path}\\{photo.filename}"
                base, extension = os.path.splitext(new_filepath)
                file_number = 1
                while new_filepath in exist_file_paths:
                    new_filepath = f"{base} ({file_number}){extension}"
                    file_number += 1
                exist_file_paths.add(new_filepath)

                # Создание задачи
                tasks.append(
                    asyncio.create_task(photo.copy_file(path=new_filepath))
                )
            await asyncio.gather(*tasks)
            progress_bar.update(len(photos[step_from:step_from + step_len]))
        progress_bar.close()

        return