import os

from pdf_to_jpg import convert_pdf_to_jpg


def prepare_file(filepath):
    global ispdf

    if filepath[len(filepath) - 3:] == 'pdf':
        ispdf = True
        print('Обнаружен PDF')
        print('\nКонвертация в JPG...')
        convert_pdf_to_jpg(filepath, os.getcwd(), 100)
        print(filepath)
        filepath = 'page_1.jpg'
        print('Готово')
        return filepath
