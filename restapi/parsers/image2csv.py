import sys

import table_ocr.util
import table_ocr.pdf_to_images
import table_ocr.extract_tables
import table_ocr.extract_cells
import table_ocr.ocr_image
import table_ocr.ocr_to_csv
import pytesseract


def convert_image_to_csv(image_filepath) -> str:
    """ Распознает текст с таблицы

    Parameters:
        image_filepath - путь до изображения с таблицей

    Returns:
        str - полученная csv
    """
    pytesseract.pytesseract.tesseract_cmd = r'parsers/tesseract\tesseract.exe'
    try:
        image_tables = table_ocr.extract_tables.main([image_filepath])
    except TypeError:
        raise ImageException
    for image, tables in image_tables:
        print(f"Processing tables for {image}.")
        for table in tables:
            print(f"Processing table {table}.")
            cells = table_ocr.extract_cells.main(table)
            ocr = [
                table_ocr.ocr_image.main(cell, tess_args=["--psm", "7", "-l", "rus", "tessdata"])
                for cell in cells
            ]
            print("Extracted {} cells from {}".format(len(ocr), table))
            return table_ocr.ocr_to_csv.text_files_to_csv(ocr)


class ImageException(Exception):
    def __init__(self, message='Не удалось найти изображение или таблицы в нём'):
        self.message = message
        super().__init__(self.message)


# Консольная утилита, для запуска ввести: python image2csv.py {название файла, лежащего в директории} {название файла - результата парсинга}
if __name__ == "__main__":
    with open(sys.argv[1], 'w') as file:
        file.write(convert_image_to_csv(sys.argv[2]))
