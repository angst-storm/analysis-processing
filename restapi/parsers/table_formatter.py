import os
import sys
import csv
import pandas as pd
from io import StringIO
from Levenshtein import distance

if os.path.exists('indicators.csv'):
    indicators = pd.read_csv('indicators.csv')
elif os.path.exists('parsers/indicators.csv'):
    indicators = pd.read_csv('parsers/indicators.csv')


def format_table(table, lab):
    table_dict = {}
    levenshtein = indicators[lab].dropna()
    for index, item in table.iterrows():
        indicator = format_word(item.indicator, levenshtein)
        indicator = indicators[((item.unit == '%') == (indicators.unit == '%')) & (indicators[lab] == indicator)]
        if len(indicator) > 0:
            table_dict[indicator['name'].iloc[0]] = float(item.value) * indicator[lab + ' cft'].iloc[0]

    formatted_table = [[indicator['name'], indicator.code, indicator.unit,
                        (table_dict[indicator['name']] if indicator['name'] in table_dict else None)]
                       for index, indicator in indicators.iterrows()]

    result = StringIO()
    csv.writer(result).writerows([['indicator', 'code', 'unit', 'value']] + formatted_table)
    return result.getvalue()


def format_word(word, levenshtein_dict):
    opt_distance = 5
    opt_word = min([(distance(word, term), term) for term in levenshtein_dict], key=lambda t: t[0])
    return opt_word[1] if opt_word[0] <= opt_distance else word
