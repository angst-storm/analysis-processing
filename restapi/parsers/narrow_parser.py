import os
import re
import sys
import shutil
import pathlib
from PIL.Image import Image
from pdf2image import convert_from_path
from .pixelscan import get_scan_result
from .cropper import get_cropped_images
from .formatter import format_table

app_dir = 'parsers/'


def parse(filepath):
    split = re.split('[./]', filepath)
    name, extension = split[-2], split[-1]

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

    lab = get_scan_result(image_paths[0])

    cropped_images_paths = [get_cropped_images(img_path, lab) for img_path in image_paths]

    # TODO: метод, возвращающий csv представление распознанных столбцов
    table = ''

    table = format_table(lab, table)

    return table


def pdf_to_image(filepath, work_dir):
    image_paths = []
    pages = convert_from_path(filepath, dpi=400, poppler_path=os.getcwd() + fr"/{app_dir}poppler-21.11.0/Library/bin")
    for index, page in enumerate(pages):
        image_path = pathlib.Path(f'{work_dir}/page_{index}.png')
        Image.save(page, image_path)
        image_paths.append(str(image_path))
    return image_paths


if __name__ == '__main__':
    app_dir = ''
    print(parse(sys.argv[1]))
