import os
import shutil


def collect_garbage(original_filepath, filepath, delete_file, is_pdf):
    """ Отчищает директорию от лишних файлов

    Parameters:
        original_filepath - путь до оригинального файла
        filepath - путь до лишних файлов, оставленных после парсинга
        delete_file - удаление оригинального файла
        is_pdf - расширение оригинального файла
    """
    if delete_file:
        os.remove(original_filepath)
    # -4 это расширение и точка, -7 это "\page_1"
    if is_pdf:
        shutil.rmtree(f'{filepath[:len(filepath) - 4 - 7]}')
    else:
        shutil.rmtree(os.getcwd() + f'\\{original_filepath}'.replace('/', '\\')[:-4])