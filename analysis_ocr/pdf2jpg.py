import os
import subprocess
import ast
import shutil
import platform
import img2pdf


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
