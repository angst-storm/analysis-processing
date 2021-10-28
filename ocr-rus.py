import table_ocr.util
import table_ocr.extract_tables
import table_ocr.extract_cells
import table_ocr.ocr_image
import table_ocr.ocr_to_csv
import pytesseract


def convert_image_to_csv(image_filepath):
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract.exe'
    image_tables = table_ocr.extract_tables.main([image_filepath])
    print(image_tables)
    for image, tables in image_tables:
        print(f"Processing tables for {image}.")
        for table in tables:
            print(f"Processing table {table}.")
            cells = table_ocr.extract_cells.main(table)
            ocr = [table_ocr.ocr_image.main(cell, tess_args=["--psm", "7", "-l", "rus",
                                                             r"Tesseract-OCR\tessdata"])
                   for cell in cells]
            print(f"Extracted {len(ocr)} cells from {table}")
            return table_ocr.ocr_to_csv.text_files_to_csv(ocr)


print("Path to image:")
csv_output = convert_image_to_csv(input())
print("CSV output:")
print(csv_output)
