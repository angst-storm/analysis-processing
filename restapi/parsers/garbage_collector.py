import os
import shutil


def collect_garbage(original_filepath, filepath, is_pdf):
    """ Отчищает директорию от лишних файлов

    Parameters:
        original_filepath - путь до оригинального файла
        filepath - путь до лишних файлов, оставленных после парсинга
        is_pdf - расширение оригинального файла
    """
    # -4 это расширение и точка, -7 это "\page_1"
    if is_pdf:
        shutil.rmtree(f'{filepath[:len(filepath) - 4 - 7]}')
    else:
        shutil.rmtree(os.getcwd() + f'\\{original_filepath}'.replace('/', '\\')[:-4])
