from .formatter import format_table
import sys
import os
import pathlib
import shutil
import re
import csv
from PIL.Image import Image
from pdf2image import convert_from_path
from table_ocr import extract_tables, extract_cells, ocr_image, ocr_to_csv
from pytesseract import pytesseract
from io import StringIO
from Levenshtein import distance
from .pixelscan import get_scan_result
from .cropper import get_cropped_images

#TODO: Поправьте импорты


#TODO: И вот это ниже (оно вообще тут надо?)
app_dir = 'parsers/'

if os.path.exists(f'{app_dir}lev_terms.txt'):
    with open(f'{app_dir}lev_terms.txt') as f:
        lev_terms = [term.strip() for term in f.readlines()]


def parse(filepath):
	split = re.split('[./]', filepath)
    name, extension = split[-2], split[-1]

    print(f'{name}.{extension}: [', end='')

    if not os.path.exists(f'{app_dir}temporary_data'):
        os.mkdir(f'{app_dir}temporary_data')

    work_dir = f'{app_dir}temporary_data/{name}'
    os.mkdir(work_dir)

    # Разибиваем пдф на картинки
    if extension == 'pdf':
        print('Converting PDF to PNG | ', end='')
        image_paths = pdf_to_image(filepath, work_dir)
    else:
        print('Document is image | ', end='')
        image_path = f'{work_dir}/page_1.{extension}'
        shutil.copy(filepath, image_path)
        image_paths = [image_path]

    print('')
    # Определяем принадлежность клинике
    target = get_scan_result(image_paths[0])
    cropped_images_paths = []
    for img_path in image_paths:
            cropped_images_paths.append(get_cropped_images(img_path, target))
    print(f'[MAIN] Cropped images: {cropped_images_paths}')


    print('\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    exit(0)

    #TODO: Тут будет часть Илюши

    # метод, возвращающий csv представление распознанных столбцов
    table = ''

    # метод, приводящий таблицу к единому формату
    table = format_table(lab, table)

    return table