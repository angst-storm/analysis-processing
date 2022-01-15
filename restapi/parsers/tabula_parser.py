import tabula
from PIL import Image
import pandas as pd



def get_table_from_images(image_path, lab):
    stream = True
    lattice = False
    if lab == 'УГМК':
        stream = False
        lattice = True
    pdf_dfs = tabula.read_pdf(image_path, pages="all", multiple_tables=True, stream=stream, lattice=lattice, guess=True)

    #TODO: сделать валидацию пустых строк (если 2+ поля в строке пусты, слить эту строку со строкой выше)
    # и проверку содержимого DataFrame'а (проверить 2-3 строки на наличие слов-индикаторов, если такие слова имеются, добавить текущий датафрейм к финальному)

    return pdf_dfs[0].to_csv

    #Цикл для проверки содержимого датафреймов
    #for i in range(len(pdf_dfs)):
        #pdf_dfs[i].to_csv(f'output{i}.csv')


