import os

from .pdf_to_jpg import convert_pdf_to_jpg


def prepare_file(filepath):
    # В этой функции происходит "подготовка" к работе:
    # Если файл - пдф, то тогда происходит конвертация
    # Так же происходит выдача пути для работы
    if filepath[len(filepath) - 3:] == 'pdf':
        print('Обнаружен PDF')
        print('\nКонвертация в JPG...')
        convert_pdf_to_jpg(filepath, os.getcwd(), 100)
        print(filepath)
        filepath = os.getcwd() + f'\\parsers\\temporary_data\\{filepath.split("/")[-1].split(".")[0]}' + '\\page_1.jpg'
        print('Готово')
        return filepath
    # Эта строчка по идее должна была дать абсолютный путь до картинок
    return os.getcwd() + f'\\{filepath}'.replace('/','\\')