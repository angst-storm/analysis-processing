import Levenshtein

show_advanced_output = False

def optimize_output(csv_output_str):
    optimized_csv_output_str = ''
    lines = csv_output_str.replace('\r', '').lower().split('\n')
    for line in lines:
        str_list = line.split(',')
        new_line_list = list(map(lambda x: get_optimized_string(x), str_list))

        if show_advanced_output:
            print(new_line_list)

        optimized_csv_output_str += '\t'.join(new_line_list)
        optimized_csv_output_str += '\r\n'
    return optimized_csv_output_str


def get_optimized_string(s):
    # Высчитывает расстояние Левенштейна со списком слов
    # и выбирает максимально подходящее (если такое есть)
    words = ['лейкоциты', 'лимфоциты', 'моноциты',
             'нейтрофилы', 'эозинофилы', 'базофилы',
             'эритроциты', 'гемоглобин', 'гематокрит',
             'тромбоциты']
    min_distance = 1000
    min_distance_word = s
    for word in words:
        distance = Levenshtein.distance(s, word)
        # Если из одной строки к другой можно прийти меньше, чем за
        # 5 изменений, то это претендет на замену
        if distance < 5 and distance < min_distance:
            min_distance = distance
            min_distance_word = word
    return min_distance_word
