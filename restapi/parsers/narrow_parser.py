import os
import re
import sys
import shutil
import pathlib
import pandas as pd
import tabula
from PIL import Image
from pdf2image import convert_from_path
from .pixel_scanner import get_scan_result
from .values_cropper import crop_images
from .table_optimizer import optimize_table
from .table_formatter import format_table
from pytesseract import pytesseract
from table_ocr import extract_tables, extract_cells, ocr_image, ocr_to_csv

app_dir = 'parsers/'


def parse(filepath):
    split = re.split(r'[./\\]', filepath)
    name, extension = split[-2], split[-1]

    if not os.path.exists(f'{app_dir}temporary_data'):
        os.mkdir(f'{app_dir}temporary_data')

    work_dir = f'{app_dir}temporary_data/{name}'
    os.mkdir(work_dir)
    os.mkdir(f'{work_dir}/images')

    if extension == 'pdf':
        pdf_path = f'{work_dir}/document.pdf'
        shutil.copy(filepath, pdf_path)
        images_paths = pdf_to_image(filepath, work_dir)
        lab = get_scan_result(images_paths[0])
        if lab == 'unknown':
            tables_found, table = tesseract_parse(images_paths)
            shutil.rmtree(work_dir)
            return tables_found, False, lab, table
        if lab == 'KDL':
            table = crop_tesseract_parse(images_paths, lab)
        else:
            table = tabula_parse(pdf_path, lab)
            table = optimize_table(table, lab)
    else:
        image_path = f'{work_dir}/images/page_0.{extension}'
        shutil.copy(filepath, image_path)
        images_paths = [image_path]
        lab = get_scan_result(images_paths[0])
        if lab in ['unknown', 'INVITRO', 'Гемотест']:
            tables_found, table = tesseract_parse(images_paths)
            shutil.rmtree(work_dir)
            return tables_found, False, lab, table
        else:
            table = crop_tesseract_parse(images_paths, lab)

    table = format_table(table, lab)

    shutil.rmtree(work_dir)

    return True, True, lab, table


def pdf_to_image(filepath, work_dir):
    image_paths = []
    pages = convert_from_path(filepath, dpi=400, poppler_path=os.getcwd() + fr"/{app_dir}poppler-21.11.0/Library/bin")
    for index, page in enumerate(pages):
        image_path = pathlib.Path(f'{work_dir}/page_{index}.png')
        Image.Image.save(page, image_path)
        image_paths.append(str(image_path))
    return image_paths


def image_to_pdf(filepath, work_dir):
    image = Image.open(filepath)
    convert_image = image.convert('RGB')
    pdf_path = f'{work_dir}/document.pdf'
    convert_image.save(pdf_path)
    return pdf_path


def tabula_parse(path, lab):
    stream = lab != 'УГМК'
    lattice = lab == 'УГМК'
    dataframes = tabula.read_pdf(path, pages="all", multiple_tables=True, stream=stream, lattice=lattice, guess=True)

    return ''.join([df.to_csv(index=None) for df in dataframes])


if os.path.exists('labs.csv'):
    labs = pd.read_csv('labs.csv')
elif os.path.exists('parsers/labs.csv'):
    labs = pd.read_csv('parsers/labs.csv')


def crop_tesseract_parse(images_paths, lab):
    if lab in ['УГМК', 'Ситилаб', 'KDL']:
        crops = crop_images(images_paths, lab)
        pytesseract.tesseract_cmd = f'{app_dir}tesseract/tesseract.exe'
        values = ''.join([pytesseract.image_to_string(crop) for crop in crops])
        values = [v for v in values.split('\n') if len(v.strip()) != 0 and not re.match('[a-zA-Z]', v)]
        table = pd.DataFrame(zip(labs[f'{lab} indicator'], values, labs[f'{lab} unit']), columns=['indicator', 'value', 'unit'])
        return table
    else:
        raise NotImplementedError


def tesseract_parse(images_paths):
    pytesseract.tesseract_cmd = f'{app_dir}tesseract/tesseract.exe'
    image_tables = extract_tables.main(images_paths)
    if len(image_tables) == 0:
        return False, 'no result'
    table = ''
    for image, tables in image_tables:
        for table in tables:
            cells = extract_cells.main(table)
            ocr = [ocr_image.main(cell, tess_args=["--psm", "7", "-l", "rus", "tessdata"]) for cell in cells]
            table += ocr_to_csv.text_files_to_csv(ocr)
    return True, table


if __name__ == '__main__':
    with open(f'parsers/{sys.argv[1]}.csv', 'w', encoding='utf-8') as f:
        f.write(parse(sys.argv[2]))
