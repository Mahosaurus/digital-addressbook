""" OCR module """
import json
import os
import sys

def main(input_folder: str, input_keyword: str):
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_cand = os.path.join(root, file)
            if os.path.isfile(file_cand) and file_cand.endswith(".json"):
                search(file_cand, input_keyword)

def search(file_cand, input_keyword):
    with open(file_cand, "r", encoding='utf-8') as fhandle:
        data = json.load(fhandle)
    if input_keyword in data:
        print(file_cand)

if __name__ == "__main__":
    input_folder = sys.argv[1]
    input_keyword = sys.argv[2]
    main(input_folder, input_keyword)
