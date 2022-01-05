import pathlib
import sys
import os
import re
from PIL.Image import Image
from pdf2image import convert_from_path
import table_ocr.util
import table_ocr.pdf_to_images
import table_ocr.extract_tables
import table_ocr.extract_cells
import table_ocr.ocr_image
import table_ocr.ocr_to_csv
import pytesseract
import shutil


# TODO: добавить оптимизацию текста
# TODO: реализовать менее костыльную валидацию PDF
def parse(filepath):
    split = re.split('[./]', filepath)
    name, extension = split[-2], split[-1]

    print(f'{name}: [', end='')
    work_dir = f'parsers/temporary_data/{name}'
    os.mkdir(work_dir)

    if extension == 'pdf':
        print('Convert PDF to PNG | ', end='')
        image_paths = pdf_to_image(filepath, work_dir)
    else:
        image_path = f'{work_dir}/page_1.{extension}'
        shutil.copy(filepath, image_path)
        image_paths = [image_path]

    print('Tables search | ', end='')
    pytesseract.pytesseract.tesseract_cmd = r'parsers\tesseract\tesseract.exe'
    image_tables = table_ocr.extract_tables.main(image_paths)
    if len(image_tables) == 0:
        print('No tables found | ', end='')
        print('Garbage cleaning]')
        shutil.rmtree(work_dir)
        raise ValueError

    print('Tables parsing | ', end='')
    csv_output_str = tables_to_csv(image_tables)

    print('Garbage cleaning]')
    shutil.rmtree(work_dir)

    return csv_output_str


def pdf_to_image(filepath, work_dir):
    image_paths = []
    pages = convert_from_path(filepath, dpi=400, poppler_path=os.getcwd() + r"/parsers/poppler-21.11.0/Library/bin")
    for index, page in enumerate(pages):
        image_path = pathlib.Path(f'{work_dir}/page_{index}.png')
        Image.save(page, image_path)
        image_paths.append(str(image_path))
    return image_paths


def tables_to_csv(image_tables):
    result = ''
    for image, tables in image_tables:
        for table in tables:
            cells = table_ocr.extract_cells.main(table)
            ocr = [table_ocr.ocr_image.main(cell, tess_args=["--psm", "7", "-l", "rus", "tessdata"]) for cell in cells]
            result += table_ocr.ocr_to_csv.text_files_to_csv(ocr)
    return result


if __name__ == '__main__':
    print(parse(sys.argv[1]))
