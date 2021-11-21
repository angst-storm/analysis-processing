import os
import shutil
import sys
from ocr import convert_image_to_csv
import pdf2jpg
import Levenshtein as lev

# Вывод логов
show_advanced_output = False
# Эта штука ответственная за удаление цели после обработки
delete_file = False


def log(s):
	# В будущем возможно добавим логи
	if show_advanced_output:
		print(s)


def execute_preparing_stage(filepath):
	global ispdf
	if filepath[len(filepath) - 3:] == 'jpg':
		log('Обнаружен JPG')

	elif filepath[len(filepath) - 3:] == 'pdf':
		ispdf = True
		log('Обнаружен PDF')
		log('\nКонвертация в JPG...')
		pdf2jpg.convert_pdf2jpg(filepath, filepath[:len(filepath) - 4], dpi=300, pages="0")
		filepath = filepath[:len(filepath) - 4] + '\\' + filepath[:len(filepath) - 4] + '.pdf_dir\\0_' + filepath[:len(
			filepath) - 4] + '.pdf.jpg'
		log('Готово')
	return filepath


def execute_text_recognition_stage():
	text = convert_image_to_csv(filepath)
	if show_advanced_output:
		log("\n---------------------------\n")
		log(text)
		log("\n---------------------------\n")
	return text


def execute_optimize_stage():
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


def execute_csv_write_stage(optimized_csv_output_str):
	f = open('done.csv', 'w')
	f.write(optimized_csv_output_str)
	f.close()


def execute_cleaning_stage():
	if delete_file:
		os.remove(original_filepath)
	shutil.rmtree(f'{filepath[:len(filepath) - 4]}')
	if ispdf:
		shutil.rmtree(f'{original_filepath[:len(original_filepath) - 4]}')


def get_optimized_string(s):
	# Высчитывает расстояние Левенштейна со списком слов
	# и выбирает максимально подходящее (если такое есть)
	words = ['лейкоциты', 'лимфоциты', 'моноциты',
			 'нейтрофилы', 'эозинофилы', 'базофилы',
			 'эритроциты','гемоглобин','гематокрит',
			 'тромбоциты']
	min_distance = 1000
	min_distance_word = s
	for word in words:
		distance = lev.distance(s, word)
		# Если из одной строки к другой можно прийти меньше, чем за
		# 5 изменений, то это претендет на замену
		if distance < 5 and distance < min_distance:
			min_distance = distance
			min_distance_word = word
	return min_distance_word


log('Запуск...')

ispdf = False
filepath = input()
original_filepath = filepath

log('\nОбработка файла...')
filepath = execute_preparing_stage(filepath)

log('\nЗапуск распознавающего модуля...')
csv_output_str = execute_text_recognition_stage()

log('\nОптимизация текста...')
optimized_csv_output_str = execute_optimize_stage()

log('\nЗапись CSV файла...')
execute_csv_write_stage(optimized_csv_output_str)

log('\nОчистка мусора...')
execute_cleaning_stage()