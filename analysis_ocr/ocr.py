import requests
import table_ocr.util
import table_ocr.pdf_to_images
import table_ocr.extract_tables
import table_ocr.extract_cells
import table_ocr.ocr_image
import table_ocr.ocr_to_csv
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image


def convert_image_to_csv(image_filepath):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract\tesseract.exe'
    image_tables = table_ocr.extract_tables.main([image_filepath])
    print(image_tables)
    for image, tables in image_tables:
        print(f"Processing tables for {image}.")
        for table in tables:
            print(f"Processing table {table}.")
            cells = table_ocr.extract_cells.main(table)
            ocr = [
                table_ocr.ocr_image.main(cell, tess_args = ["--psm", "7", "-l", "rus", "tessdata"])
                for cell in cells
            ]
            print("Extracted {} cells from {}".format(len(ocr), table))
            return table_ocr.ocr_to_csv.text_files_to_csv(ocr)
