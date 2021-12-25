import os
import os
import shutil

from .image2csv import convert_image_to_csv
from .optimizer import optimize_output
from .file_preparer import prepare_file
from .garbage_collector import collect_garbage
from .csv_writer import write_csv

show_advanced_output = True
# Эта штука ответственная за удаление оригинального файла после обработки
delete_file = True
# Нужно ли создавать csv?
create_csv = False

#TODO: При загрузке пдф без таблицы ошибка с NoneType
#TODO: Полнейшая ж*** при загрузке картинок! Пофиксить. ПДФ работает нормально (кроме пункта выше)
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
    if original_filepath[len(original_filepath) - 3:] == 'pdf':
        ispdf = True

    log('\nЗапуск распознавающего модуля...')
    csv_output_str = convert_image_to_csv(filepath)

    # На данном этапе "оптимизация" съедает запятые, что ломает файл
    #log('\nОптимизация текста...')
    #optimized_csv_output_str = optimize_output(csv_output_str)
    optimized_csv_output_str = csv_output_str

    log('\nЗапись CSV файла...')
    write_csv(optimized_csv_output_str, create_csv)

    log("\nУдаление лишних файлов...")
    collect_garbage(original_filepath, filepath, delete_file, ispdf)
    return optimized_csv_output_str
