import os

from .pdf_to_jpg import convert_pdf_to_jpg


def prepare_file(filepath):
    global ispdf

    if filepath[len(filepath) - 3:] == 'pdf':
        ispdf = True
        print('Обнаружен PDF')
        print('\nКонвертация в JPG...')
        convert_pdf_to_jpg(filepath, os.getcwd(), 100)
        print(filepath)
        filepath = os.getcwd() + f'\\temporary_data\\{filepath.split("/")[-1].split(".")[0]}' + '\\page_1.jpg'
        print('Готово')
        return filepath
    # Эта строчка по идее должна была дать абсолютный путь до картинок
    return os.getcwd() + f'\\{filepath}'.replace('/','\\')