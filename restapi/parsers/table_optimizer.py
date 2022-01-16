import re
import csv
import pandas as pd
from io import StringIO


def optimize_table(table, lab):
    if lab == 'УГМК':
        table = csv.reader(table.split('\r\n'))
        table = [row[:3] for row in table if len(row) == 5]
        table = pd.DataFrame(table, columns=['indicator', 'value', 'unit'])

    elif lab == 'Ситилаб':
        table = csv.reader(table.split('\r\n'))
        table = [row for row in table if len(row) == 3]
        for row in table:
            if len(row[1]) == 0:
                sep_index = row[0].rfind(' ')
                row[1] = row[0][sep_index + 1:]
                row[0] = row[0][:sep_index]
            sep_index = row[2].find(' ')
            if sep_index == -1:
                del row
            else:
                row[2] = row[2][:sep_index]
        table = pd.DataFrame(table, columns=['indicator', 'value', 'unit'])
        table = table.dropna()

    elif lab == 'INVITRO':
        table = StringIO(table)
        table = pd.read_csv(table)
        rename_dict = {'Исследование': 'indicator', 'Результат': 'value', 'Единицы': 'unit'}
        table.rename(columns=rename_dict, inplace=True)

    elif lab == 'Гемотест':
        table = csv.reader(table.split('\r\n'))
        table = [row[:3] for row in table if len(row) == 4]
        table = pd.DataFrame(table, columns=['indicator', 'value', 'unit'])

    else:
        raise NotImplementedError

    # TODO: падает при появлении nan в таблице
    table.value = table.value.apply(lambda v: re.sub('[*+-]', '', v))
    return table[['indicator', 'value', 'unit']]
