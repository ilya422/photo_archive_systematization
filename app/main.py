import argparse
import logging

from classes.image_systematization import ImageSystematization, ImageSystematizationException

logging.basicConfig(level=logging.INFO)

# Получение аргументов запуска приложения
parser = argparse.ArgumentParser(
    description="Программа для систематизации домашнего фотоархива"
)
parser.add_argument("source_dir", help="Исходный каталог")
parser.add_argument("result_dir", help="Результирующий каталог")

args = parser.parse_args()

# Запуск систематизации
try:
    ImageSystematization.run(source_dir=args.source_dir, result_dir=args.result_dir)
except ImageSystematizationException as ex:
    logging.error(str(ex))
    exit(1)