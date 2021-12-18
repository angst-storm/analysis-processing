import os
from pdf2image import convert_from_path

# input_path - путь до файла, который нужно парсить
# output_path - путь до места, в котором будет папка с зажипеженной пдфкой
# либо можно вернуть pages - массив страниц в жпг


def convert_pdf_to_jpg(input_path, output_path, dpi):
    pages = convert_from_path(input_path, dpi=dpi, poppler_path=r"poppler-21.11.0\Library\bin")


    pages_counter = 0
    for page in pages:
        pages_counter += 1
        page.save(f'{output_path}/page_{pages_counter}.jpg', 'JPEG')


# тест
# convert_pdf_to_jpg("some_file.pdf", os.getcwd(), 100)