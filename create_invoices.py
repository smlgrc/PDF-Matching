import os
import sys
import json
import PyPDF2
import pandas
from PyPDF2 import PageObject, PdfReader
from datetime import datetime

with open(os.path.join(r"C:\GitHub-Config-files\PDF-Matching.json"), 'r', encoding='utf-8') as jsonFile:
    dict_of_paths: dict = json.load(jsonFile)

file_folder_path: str = os.path.join(rf"{dict_of_paths['file_folder']}")
location_folder_path: str = os.path.join(rf"{dict_of_paths['location_folder']}")
invoice_folder_path: str = os.path.join(rf"{dict_of_paths['invoice_folder']}")
logs_folder_path: str = os.path.join(rf"{dict_of_paths['logs_folder']}")
letter_file_path: str = os.path.join(rf"{dict_of_paths['letter_file']}")
case_file_path: str = os.path.join(rf"{dict_of_paths['case_file']}")
# TODO: KAMI'S FILES WILL JUST BE HARDCODED, THEN AN EXECUTABLE WILL TAKE CARE OF THE REST

master_dict: dict = {}
master_list: list = []
read_pages_dict: dict = {}


def initialize_master_dict():
    global master_list, master_dict
    ext: str = '.xlsx'
    excel_file_name: str = 'Sheet1.xlsx'
    excel_file_path: str = os.path.join(file_folder_path, excel_file_name)

    # base_ref_num_list: list = []
    eng: str = "xlrd"

    if ext.lower() == '.xlsx' or ext.lower() == '.xlsm':
        eng = "openpyxl"
    elif ext.lower() == '.xlsb':
        eng = "pyxlsb"

    column_name: str = 'Order No'
    df = pandas.read_excel(excel_file_path)[[column_name]]
    for i in range(len(df)):
        master_list.append(str(df[column_name].iloc[i]))

    # initialize master_list
    for ref in master_list:
        master_dict[ref] = {}


def process_letters_pdf():
    global master_dict, letter_file_path
    page: int = 0
    pdfFileObj = open(letter_file_path, 'rb')
    try:
        pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
        pdfPages: list[PageObject] = pdfReader.pages

        for i in range(len(pdfPages)):
            pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
            page_num = pdfReader.get_page_number(pageObj)
            pageTxt: str = pageObj.extract_text().lower()

            if pageTxt == '' or pageTxt.isspace():
                continue

            split_word = 'Ref: '.lower()
            base_ref_num = pageTxt.partition(split_word)[2].partition("\n")[0].strip()

            ref_num_match = {
                'file_path': letter_file_path,
                'page_num': page_num
            }
            page += 1
            ref_num_letter = f'{base_ref_num}-letter-{str(page)}'
            master_dict[base_ref_num][ref_num_letter] = ref_num_match
            if page == 2:
                page = 0

    except Exception as e:  # PyPDF2.errors.PdfReadError:
        print(f'{e} <- here')
    pdfFileObj.close()


def process_case_pdf():
    global master_dict, case_file_path
    pdfFileObj = open(case_file_path, 'rb')
    try:
        pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
        pdfPages: list[PageObject] = pdfReader.pages
        for i in range(len(pdfPages)):
            pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
            pageTxt: str = pageObj.extract_text().lower()

            if pageTxt == '' or pageTxt.isspace():
                continue

            split_word = 'Ref#: '.lower()
            base_ref_num = pageTxt.partition(split_word)[2].partition(" ")[0].strip()
            page_num = pdfReader.get_page_number(pageObj)

            ref_num_match = {
                'file_path': case_file_path,
                'page_num': page_num
            }
            ref_num_case = f'{base_ref_num}-case'
            master_dict[base_ref_num][ref_num_case] = ref_num_match

    except Exception as e:
        print(f'{e} <- here')
    pdfFileObj.close()


def process_location_folder():
    global master_dict
    for subdir, dirs, files in os.walk(location_folder_path):
        """
        subdir = current parent folder name
        dirs = list of directory names in subdir
        files = list of file names in subdir
        """
        for file in files:
            file_path = os.path.join(subdir, file)
            root_and_ext = os.path.splitext(file_path)
            root = root_and_ext[0]
            ext = root_and_ext[1]

            pdfFileObj = open(file_path, 'rb')
            try:
                pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
                pdfPages: list[PageObject] = pdfReader.pages

                for i in range(len(pdfPages)):
                    pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
                    page_num = pdfReader.get_page_number(pageObj)
                    pageTxt: str = pageObj.extract_text().lower()

                    if pageTxt == '' or pageTxt.isspace():
                        continue

                    split_word = 'Invoice Number: '.lower()
                    ref_num_extract = pageTxt.partition(split_word)[2].replace(' ', '').partition("invoice")[0]
                    base_num_extract = ref_num_extract.partition('-')[0]
                    # breakpoint()

                    ref_num_match = {
                        'file_path': file_path,
                        'page_num': page_num
                    }

                    master_dict[base_num_extract][ref_num_extract] = ref_num_match

            except Exception as e:  # PyPDF2.errors.PdfReadError:
                print(f'{e} <- here')
            pdfFileObj.close()


def save_json_log():
    global master_dict
    logs_path = os.path.join(logs_folder_path, 'master_dict_log.txt')
    with open(logs_path, 'w') as master_dict_log:
        master_dict_log.write(json.dumps(master_dict, indent=4))


def search_and_save_locations():
    process_letters_pdf()
    process_case_pdf()
    process_location_folder()
    save_json_log()


def merge_pdfs():
    global master_dict
    for base_ref_num, ref_num_matches in master_dict.items():
        print(f'Processing {base_ref_num}...')
        pdfOutputPath = os.path.join(invoice_folder_path, f'{base_ref_num}-invoices.pdf')
        pdfOutputFile = open(pdfOutputPath, 'wb')
        pdfWriter = PyPDF2.PdfWriter()

        # ref_num_keys = list(ref_num_matches.keys())
        # ref_num_keys.sort()
        # ref_num_keys = sort_ref_num_list(ref_num_keys)
        # sorted_ref_num_matches = {key: ref_num_matches[i] for key in ref_num_keys}
        for ref_num_match, ref_num_attributes in ref_num_matches.items():#sorted_ref_num_matches.items()
            file_path = os.path.join(ref_num_attributes['file_path'])
            page_num: str = ref_num_attributes['page_num']

            pdfFileObj = open(file_path, 'rb')
            try:
                pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
                pageObj = pdfReader.pages[int(page_num)]
                pdfWriter.add_page(pageObj)

                pdfWriter.write(pdfOutputFile)
            except Exception as e:  # PyPDF2.errors.PdfReadError:
                print(e)
            pdfFileObj.close()
        pdfOutputFile.close()


def run_script():
    start_time = datetime.now()

    initialize_master_dict()
    # initialize_read_pages_dict()  # not used

    print('combining and sorting')
    search_and_save_locations()

    print('merging pdfs')
    merge_pdfs()

    end_time = datetime.now()
    run_time = end_time - start_time
    print('\nProgram Run Time:', run_time)

    user_input = input('Press ENTER to exit: ')
    sys.exit(0)


def main():
    # demo()
    run_script()


if __name__ == '__main__':
    main()
