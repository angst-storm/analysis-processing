import os
import shutil


def collect_garbage(original_filepath, filepath, delete_file, ispdf):
    if delete_file:
        os.remove(original_filepath)
    # Удаление папки с картинкой после конвертации в jpg
    # Даст строку вида "\restapi\temporary_data\target_hI7CZ3G"
    # -4 это расширение и точка, -7 это "\page_1"
    if ispdf:
        shutil.rmtree(f'{filepath[:len(filepath) - 4 - 7]}')

    if not ispdf:
        print(os.getcwd()+f'\\{original_filepath}'.replace('/', '\\')[:-4])
        shutil.rmtree(os.getcwd()+f'\\{original_filepath}'.replace('/', '\\')[:-4])