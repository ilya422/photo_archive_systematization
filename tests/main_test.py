import os
import shutil

from classes.image_systematization import ImageSystematization


def test_image_systematization():
    source_dir = './source_dir'
    result_dir = './result_dir'
    shutil.rmtree(result_dir)

    current_result_dirs = {
        '2024': 4,
        '2025': 2
    }

    # Запуск систематизации изображений
    ImageSystematization.run(source_dir=source_dir, result_dir=result_dir)

    # Проверка правильности папок
    result_dirs = os.listdir(result_dir)
    assert len(result_dirs) == len(current_result_dirs)
    for _result_dir in result_dirs:
        assert _result_dir in current_result_dirs

    # Проверка кол-ва файлов в папках
    for _result_dir in result_dirs:
        result_files = os.listdir(f"./{result_dir}/{_result_dir}")
        assert len(result_files) == current_result_dirs.get(_result_dir, 0)


