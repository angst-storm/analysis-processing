import os
import os
import shutil

from image2csv import convert_image_to_csv
from optimizer import optimize_output
from file_preparer import prepare_file
from garbage_collector import collect_garbage
from csv_writer import write_csv

show_advanced_output = False
# Эта штука ответственная за удаление цели после обработки
delete_file = True


def log(s):
    # В будущем возможно добавим логи
    if show_advanced_output:
        print(s)


def parse_pdf(filepath):
    ispdf = False
    log('Запуск...')

    original_filepath = filepath

    log('\nОбработка файла...')
    filepath = prepare_file(filepath)

    if filepath != original_filepath:
        ispdf = True

    log('\nЗапуск распознавающего модуля...')
    csv_output_str = convert_image_to_csv(filepath)

    log('\nОптимизация текста...')
    optimized_csv_output_str = optimize_output(csv_output_str)

    log('\nЗапись CSV файла...')
    write_csv(optimized_csv_output_str)

    log("\nУдаление лишних файлов...")
    collect_garbage(original_filepath, filepath, delete_file, ispdf)
    return optimized_csv_output_str
