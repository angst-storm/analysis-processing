import ast
import os
import shutil
import subprocess
import sys


def __convert_pdf2jpg_single(jarPath, inputpath, outputpath, dpi, pages):
    try:
        cmd = 'java -jar %s -i "%s" -o "%s" -d %s -p %s' % (jarPath, inputpath, outputpath, str(dpi), pages)
        outputpdfdir = os.path.join(outputpath, os.path.basename(inputpath) + "_dir")
        if os.path.exists(outputpdfdir):
            shutil.rmtree(outputpdfdir)

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
        sys.exit()
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
        sys.exit()