import Levenshtein
import os
import subprocess
import ast
import shutil
import platform
import img2pdf
from .image2csv import convert_image_to_csv
from .pdf_to_jpg import convert_pdf_to_jpg

def __convert_pdf2jpg_single(jarPath, inputpath, outputpath, dpi, pages):
    try:

        cmd = 'java -jar %s -i "%s" -o "%s" -d %s -p %s' % (jarPath, inputpath, outputpath, str(dpi), pages)
        outputpdfdir = os.path.join(outputpath, os.path.basename(inputpath) + "_dir")
        if os.path.exists(outputpdfdir):
            shutil.rmtree(outputpdfdir)

        system = platform.system()
        if system == "Linux":
            cmd = ["java", "-jar", jarPath, "-i", inputpath, "-o", outputpath, "-d", str(dpi), "-p", pages]
            output = subprocess.check_output(cmd)
        else:
            output = subprocess.check_output(cmd)

        output = output.decode('cp1252')
        output = output.split("#################################")[1].strip()

        output = ast.literal_eval(output)
        outputpdfdir = output[inputpath]

        outputFiles = map(lambda x: os.path.join(outputpdfdir, x), os.listdir(outputpdfdir))
        outputFiles = sorted(outputFiles, key=lambda x: os.path.basename(x).split("_")[0])
        result = {
            'cmd': cmd,
            'input_path': inputpath,
            'output_pdfpath': outputpdfdir,
            'output_jpgfiles': outputFiles
        }
    except Exception as err:
        print(err)
        return False
    return [result]


def convert_pdf2jpg(inputpath, outputpath, dpi=300, pages="ALL"):
    try:
        dpi = int(dpi)
        pages = pages.split(",")
        pages = map(lambda x: x.strip(), pages)
        pages = ",".join(pages)
        jarPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), r"pdf2jpg.jar")
        return __convert_pdf2jpg_single(jarPath, inputpath, outputpath, dpi=dpi, pages=pages)
    except Exception as err:
        print(err)
        return False


def convert_pdf2imgpdf(inputpath, outputpath, dpi):
    try:
        dpi = int(dpi)
        jpgOutputDir = "tmp_pdf2jpg"
        if os.path.exists(jpgOutputDir):
            shutil.rmtree(jpgOutputDir)

        output = convert_pdf2jpg(inputpath, jpgOutputDir, dpi, pages="ALL")
        if not output:
            print("Unable to convert PDF into images")
            return False

        outputjpgfiles = output[0]['output_jpgfiles']
        print(outputjpgfiles)

        outputdir = os.path.dirname(outputpath)
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        with open(outputpath, "wb") as f:
            f.write(img2pdf.convert(outputjpgfiles))
        if os.path.exists(jpgOutputDir):
            shutil.rmtree(jpgOutputDir)
    except Exception as err:
        print(err)
        return False
    return True


if __name__ == "__main__":
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    inputpath = r"D:\sourcecodes\document.pdf"
    outputpath = r"D:\sourcecodes"
    result = convert_pdf2jpg(inputpath, outputpath, dpi=80, pages="0,1,2,3")
    print('==================')
    pp.pprint(result)
    print('==================')

    outputpath = r"D:\Working Folder\file1.pdf"
    result = convert_pdf2imgpdf(inputpath, outputpath, dpi=100)
    print('==================')
    print(result)
    print('==================')

try:
    from PIL import Image
except ImportError:
    import Image





def parse_pdf(filepath):
    # Вывод логов
    show_advanced_output = False
    # Эта штука ответственная за удаление цели после обработки
    delete_file = True

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
            convert_pdf2jpg(filepath, filepath[:len(filepath) - 4], dpi=300, pages="0")
            print(filepath)
            filepath = filepath[:len(filepath) - 4] + '\\' \
                       + filepath[:len(filepath) - 4][8:] + '.pdf_dir\\0_' \
                       + filepath[:len(filepath) - 4][8:] + '.pdf.jpg'
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

    log('Запуск...')

    ispdf = False
    original_filepath = filepath

    log('\nОбработка файла...')
    filepath = execute_preparing_stage(filepath)

    log('\nЗапуск распознавающего модуля...')
    csv_output_str = execute_text_recognition_stage()

    log('\nОптимизация текста...')
    optimized_csv_output_str = execute_optimize_stage()

    log('\nЗапись CSV файла...')

    execute_cleaning_stage()
    return optimized_csv_output_str
