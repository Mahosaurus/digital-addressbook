""" OCR module """
import os
import sys

from typing import Iterator

from PIL import Image
from pdf2image import convert_from_path
import pytesseract

def main(input_folder: str):
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_cand = os.path.join(root, file)
            if os.path.isfile(file_cand):
                output_path = get_output_path(file_cand, input_folder)
                do_ocr(file_cand, output_path)
 
def get_output_path(input_path: str, input_folder: str) -> str:
    abs_output_path = os.path.abspath(input_path)
    file_name = os.path.basename(abs_output_path)
    folder_name = os.path.dirname(abs_output_path)
    common_path = os.path.commonpath([os.path.abspath(input_folder), folder_name])
    root_path = os.path.dirname(common_path)
    subdir = os.path.relpath(folder_name, common_path)
    final_path = os.path.join(root_path, "output", subdir, file_name)
    os.makedirs(os.path.join(root_path, "output", subdir), exist_ok=True)
    return final_path


def do_ocr(file_cand, output_path):
    pages = convert_from_path(file_cand, 1000, single_file=True)
    print("Starting tesseract")
    #result = pytesseract.image_to_string(pages[0], , lang='ger')
    # Get a searchable PDF  
    pdf = pytesseract.image_to_pdf_or_hocr(pages[0], extension='pdf')
    with open(output_path, 'w+b') as fhandle:
        fhandle.write(pdf) # pdf type is bytes by default


if __name__ == "__main__":
    input_folder = sys.argv[1]
    main(input_folder)
    
