import os
import shutil


def collect_garbage(original_filepath, filepath, delete_file, ispdf):
    if delete_file:
        os.remove(original_filepath)
    # Удаление папки с картинкой после конвертации в jpg
    # Даст строку вида "\restapi\temporary_data\target_hI7CZ3G"
    # -4 это расширение и точка, -7 это "\page_1"
    shutil.rmtree(f'{filepath[:len(filepath) - 4 - 7]}')


    # Скорее всего надо инвертировать флаг и чето с ним делать
    # сейчас с пдф все работает нормально (без кода ниже)

    #if ispdf:
    #    shutil.rmtree(os.getcwd()+f'\\{original_filepath}'.replace('/', '\\'))