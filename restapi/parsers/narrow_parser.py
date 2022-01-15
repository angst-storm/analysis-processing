import os
import re
import sys
import shutil
import pathlib
import tabula
from PIL import Image
from pdf2image import convert_from_path
from pixel_scanner import get_scan_result
from table_optimizer import optimize_table
from table_formatter import format_table

app_dir = 'parsers/'


def parse(filepath):
    # берем имя и расширение документа
    split = re.split(r'[./\\]', filepath)
    name, extension = split[-2], split[-1]

    # создаем папки для сохранения промежуточных файлов
    work_dir = f'{app_dir}temporary_data/{name}'
    os.mkdir(work_dir)
    os.mkdir(f'{work_dir}/images')

    # в зависимости от расширения документа производим конвертации (pdf в image или наоборот)
    if extension == 'pdf':
        pdf_path = f'{work_dir}/document.pdf'
        shutil.copy(filepath, pdf_path)
        image_paths = pdf_to_image(filepath, work_dir)
    else:
        pdf_path = image_to_pdf(filepath, work_dir)
        image_path = f'{work_dir}/images/page_0.{extension}'
        shutil.copy(filepath, image_path)
        image_paths = [image_path]

    # получаем название лаборатории, где произведен анализ
    lab = get_scan_result(image_paths[0])

    # запускаем распознание при помощи tabula
    table = tabula_parse(pdf_path, lab)
    # оптимизируем таблицу (меняем заголовки, убираем лишние знаки, ячейки и т.д.)
    table = optimize_table(table, lab)
    # приводим таблицу к единому формату
    table = format_table(table, lab)

    # удаляем промежуточные файлы
    shutil.rmtree(work_dir)

    return table


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


if __name__ == '__main__':
    with open(f'parsers/{sys.argv[1]}.csv', 'w', encoding='utf-8') as f:
        f.write(parse(sys.argv[2]))
