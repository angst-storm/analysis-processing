import os
from .pdf2jpg import convert_pdf_to_jpg
from .image2csv import convert_image_to_csv
from .optimizer import optimize_output
from .garbage_collector import collect_garbage

# включение логирования
show_advanced_output = True
# удаление оригинального файла
delete_file = True
# сохранение результата в csv
create_csv = False


# TODO: добавить логирование
def log(s):
    if show_advanced_output:
        print(f'{s}\n')


# TODO: при загрузке pdf без таблицы ошибка с NoneType
def parse_pdf(original_filepath):
    # TODO: более разумный способ проверки на pdf, расширение может быт побито, но файл оставаться pdf
    is_pdf = original_filepath[len(original_filepath) - 3:] == 'pdf'

    log('Обработка файла...')
    filepath = convert_pdf_to_jpg(original_filepath, os.getcwd(),
                                  400) if is_pdf else f'{os.getcwd()}\\{original_filepath}'.replace('/', '\\')

    log('Запуск распознавающего модуля...')
    csv_output_str = convert_image_to_csv(filepath)

    # TODO: оптимизация "съедает" запятые, исправить
    # log('\nОптимизация текста...')
    # csv_output_str = optimize_output(csv_output_str)

    if create_csv:
        log('Запись CSV файла...')
        with open('parser/done.csv', 'w') as file:
            file.write(csv_output_str)

    log("Удаление лишних файлов...")
    collect_garbage(original_filepath, filepath, delete_file, is_pdf)

    return csv_output_str
