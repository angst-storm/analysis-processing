import os
import sys

from pdf2image import convert_from_path


def convert_pdf_to_jpg(input_path, output_path, dpi) -> str:
    """ Конвертирует файл PDF в JPEG

    Parameters:
        input_path - путь до файла, который нужно конвертировать в jpeg
        output_path - путь до директории, в которой будет папка с конвертированным файлом
        dpi - количество точек на дюйм в конвертированном файле

    Returns:
        str - путь до конвертированного файла
    """
    pages = convert_from_path(input_path, dpi=dpi, poppler_path=os.getcwd() + r"\parsers\poppler-21.11.0\Library\bin")
    if not os.path.exists(output_path + f'/parsers/temporary_data'):
        os.mkdir(output_path + f'/parsers/temporary_data')
    output_path = output_path + f'/parsers/temporary_data/{input_path.split("/")[-1].split(".")[0]}'

    os.mkdir(output_path)

    for index, page in enumerate(pages):
        page.save(f'{output_path}/page_{index + 1}.jpg', 'JPEG')

    # TODO: для многостраничного файла - возвращать все страницы, а не только первую
    return f'{os.getcwd()}\\parsers\\temporary_data\\{input_path.split("/")[-1].split(".")[0]}\\page_1.jpg'


# Консольная утилита, для запуска ввести: python pdf2jpg.py {название файла, лежащего в директории} {dpi}
if __name__ == "__main__":
    convert_pdf_to_jpg(sys.argv[1], os.getcwd(), int(sys.argv[2]))
