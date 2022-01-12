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

app_dir = 'parsers/'

if os.path.exists(f'{app_dir}levenshtein_dict.txt'):
    with open(f'{app_dir}levenshtein_dict.txt') as f:
        levenshtein_dict = [term.strip() for term in f.readlines()]


def parse(filepath):
    split = re.split('[./]', filepath)
    name, extension = split[-2], split[-1]

    print(f'{name}.{extension}: [', end='')

    if not os.path.exists(f'{app_dir}temporary_data'):
        os.mkdir(f'{app_dir}temporary_data')

    work_dir = f'{app_dir}temporary_data/{name}'
    os.mkdir(work_dir)

    if extension == 'pdf':
        print('Converting PDF to PNG | ', end='')
        image_paths = pdf_to_image(filepath, work_dir)
    else:
        print('Document is image | ', end='')
        image_path = f'{work_dir}/page_1.{extension}'
        shutil.copy(filepath, image_path)
        image_paths = [image_path]

    print('Tables searching | ', end='')
    pytesseract.tesseract_cmd = f'{app_dir}tesseract/tesseract.exe'
    image_tables = extract_tables.main(image_paths)
    if len(image_tables) == 0:
        print('No tables found | ', end='')
        print('Garbage cleaning]')
        shutil.rmtree(work_dir)
        raise ValueError

    print('Tables parsing | ', end='')
    result_table = tables_to_csv(image_tables)

    print('Levenshtein optimization | ', end='')
    result_table = optimize_table(result_table)

    print('Garbage cleaning]')
    shutil.rmtree(work_dir)

    return result_table


def pdf_to_image(filepath, work_dir):
    image_paths = []
    pages = convert_from_path(filepath, dpi=400, poppler_path=os.getcwd() + fr"/{app_dir}poppler-21.11.0/Library/bin")
    for index, page in enumerate(pages):
        image_path = pathlib.Path(f'{work_dir}/page_{index}.png')
        Image.save(page, image_path)
        image_paths.append(str(image_path))
    return image_paths


def tables_to_csv(image_tables):
    result = ''
    for image, tables in image_tables:
        for table in tables:
            cells = extract_cells.main(table)
            ocr = [ocr_image.main(cell, tess_args=["--psm", "7", "-l", "rus", "tessdata"]) for cell in cells]
            result += ocr_to_csv.text_files_to_csv(ocr)
    return result


def optimize_table(table):
    """Оптимизация всего распознанного текста"""
    lines = csv.reader(table.split('\r\n'))
    opt_lines = [[optimize_word(word) for word in line] for line in lines]
    opt_table = StringIO()
    csv.writer(opt_table).writerows(opt_lines)
    return opt_table.getvalue()


def optimize_word(word):
    """Оптимизация слова. Если при распознавании в слове была допущена небольшая ошибка, то это поможет всё исправить"""
    opt_distance = 5
    opt_word = min([(distance(word.lower(), term), term) for term in levenshtein_dict], key=lambda t: t[0])
    return opt_word[1] if opt_word[0] <= opt_distance else word


if __name__ == '__main__':
    app_dir = ''
    with open('levenshtein_dict.txt') as f:
        levenshtein_dict = [term.strip() for term in f.readlines()]
    print(parse(sys.argv[1]))
