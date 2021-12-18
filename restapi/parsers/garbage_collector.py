import os
import shutil


def collect_garbage(original_filepath, filepath, delete_file, ispdf):
    if delete_file:
        os.remove(original_filepath)
    shutil.rmtree(f'{filepath[:len(filepath) - 4]}')
    if ispdf:
        shutil.rmtree(f'{original_filepath[:len(original_filepath) - 4]}')