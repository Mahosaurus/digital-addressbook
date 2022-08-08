""" OCR module """
import json
import os
import re
import sys

from PIL import Image
from pdf2image import convert_from_path
import pytesseract

def main(input_folder: str):
    """ Main function to walk thru files """
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_cand = os.path.join(root, file)
            if os.path.isfile(file_cand) and "output" not in file_cand:
                print(f"Processing {file_cand}")
                output_path = get_output_path(file_cand, input_folder)
                if os.path.isfile(output_path + ".pdf") and os.path.isfile(output_path + ".json"):
                    print(f"Skipping {file_cand} as it exists already")
                    continue
                do_ocr(file_cand, output_path)

def get_output_path(input_path: str, input_folder: str) -> str:
    """ Gets outpath """
    while len(input_folder.split("/")) > 2: # TODO: make universal for every OS
        input_folder = os.path.dirname(input_folder)
    abs_output_path = os.path.abspath(input_path)
    file_name = os.path.basename(abs_output_path).split(".")[0]
    folder_name = os.path.dirname(abs_output_path)
    common_path = os.path.commonpath([os.path.abspath(input_folder), folder_name])
    root_path = os.path.dirname(common_path)
    subdir = os.path.relpath(folder_name, common_path)
    final_path = os.path.join(root_path, "output", subdir, file_name)
    os.makedirs(os.path.join(root_path, "output", subdir), exist_ok=True)
    return final_path

def do_ocr(file_cand, output_path):
    pages = convert_from_path(file_cand, 1000, single_file=True)
    print("Starting tesseract img to str")

    # Get an indexable document
    result_text = bytes(pytesseract.image_to_string(pages[0], lang='deu'), 'utf-8').decode('utf-8')
    result_text = result_text.replace("\n", "")
    result_text = result_text.replace(",", " ")
    result_text = result_text.replace("-", " ")
    result_text = result_text.replace("—", " ")
    result_text = result_text.replace("—", " ")
    result_text = [text.lower() for text in result_text.split(" ") if text]

    with open(output_path + ".json", "w", encoding='utf-8') as fhandle:
        json.dump(result_text, fhandle, ensure_ascii=False)

    print("Starting tesseract img to pdf")
    # Get a searchable PDF
    result_pdf = pytesseract.image_to_pdf_or_hocr(pages[0], lang='deu', extension='pdf')
    with open(output_path + ".pdf", 'w+b') as fhandle:
        fhandle.write(result_pdf)

if __name__ == "__main__":
    input_folder = sys.argv[1]
    main(input_folder)
