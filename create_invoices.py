import os
import sys
import json
import PyPDF2
import pandas
from PyPDF2 import PageObject, PdfReader
from datetime import datetime


file_folder_path: str = os.path.join(r"C:\Users\samga\Documents\Work\Scandoc-Imaging\DEMO\KAMI_FILES")
location_folder_path: str = os.path.join(r"C:\Users\samga\Documents\Work\Scandoc-Imaging\DEMO\KAMI_FILES\location_folder")
invoice_folder_path: str = os.path.join(r"C:\Users\samga\Documents\Work\Scandoc-Imaging\DEMO\KAMI_FILES\invoice_folder")
logs_folder_path: str = os.path.join(r"C:\Users\samga\Documents\Work\Scandoc-Imaging\DEMO\KAMI_FILES\logs")

def ref_num_list_extract_from_excel_file() -> list:
    ext: str = '.xlsx'
    excel_file_name: str = 'Sheet1.xlsx'
    excel_file_path: str = os.path.join(file_folder_path, excel_file_name)

    base_ref_num_list: list = []
    eng: str = "xlrd"

    if ext.lower() == '.xlsx' or ext.lower() == '.xlsm':
        eng = "openpyxl"
    elif ext.lower() == '.xlsb':
        eng = "pyxlsb"

    column_name: str = 'Order No'
    df = pandas.read_excel(excel_file_path)[[column_name]]
    for i in range(len(df)):
        base_ref_num_list.append(str(df[column_name].iloc[i]))

    return base_ref_num_list


def create_master_dict(master_list) -> dict:
    base_master_dict: dict = {}
    for ref in master_list:
        base_master_dict[ref] = {}

    return base_master_dict


def process_letters_pdf(file_path, master_dict) -> dict:
    counter: int = 0
    pdfFileObj = open(file_path, 'rb')
    try:
        pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
        pdfPages: list[PageObject] = pdfReader.pages

        for i in range(len(pdfPages)):
            pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
            pageTxt: str = pageObj.extract_text().lower()
            # print(pageTxt)
            # print(f'\n\nOUTER INDEX = {i}\n\n')
            # breakpoint()

            # breakpoint()
            for j, base_ref_num in enumerate(list(master_dict.keys())):
                # print(f'\nbase ref num = {base_ref_num}')
                # print('PAGE TEXT')
                # print(pageTxt)
                # print(f'\n\nINNER INDEX = {j}\n\n')
                if base_ref_num in pageTxt:
                    # breakpoint()
                    split_word = 'Ref: '.lower()
                    ref_num_extract = pageTxt.partition(split_word)[2].partition("\n")[0].strip()
                    page_num = pdfReader.get_page_number(pageObj)
                    ref_num_match = {
                        'file_path': file_path,
                        'page_num': page_num
                    }
                    counter += 1
                    ref_num_extract = f'{ref_num_extract}-letter-{str(counter)}'
                    master_dict[base_ref_num][ref_num_extract] = ref_num_match
                    if counter == 2:
                        counter = 0
                    # print('\n\nBREAKING\n\n')
                    break

    except Exception as e:  # PyPDF2.errors.PdfReadError:
        print(e)
    pdfFileObj.close()
    return master_dict


def process_case_pdf(file_path, master_dict) -> dict:
    pdfFileObj = open(file_path, 'rb')
    try:
        pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
        pdfPages: list[PageObject] = pdfReader.pages
        for i in range(len(pdfPages)):
            pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
            pageTxt: str = pageObj.extract_text().lower()
            for j, base_ref_num in enumerate(list(master_dict.keys())):
                if base_ref_num in pageTxt:
                    # breakpoint()
                    split_word = 'Ref#: '.lower()
                    ref_num_extract = pageTxt.partition(split_word)[2].partition(" ")[0].strip()
                    page_num = pdfReader.get_page_number(pageObj)
                    ref_num_match = {
                        'file_path': file_path,
                        'page_num': page_num
                    }
                    ref_num_extract = f'{ref_num_extract}-case'
                    master_dict[base_ref_num][ref_num_extract] = ref_num_match
                    break
    except Exception as e:
        print(e)
    pdfFileObj.close()
    return master_dict


def process_location_folder(master_dict) -> dict:
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
                    pageTxt: str = pageObj.extract_text().lower()

                    for j, base_ref_num in enumerate(list(master_dict.keys())):
                        if base_ref_num in pageTxt:
                            split_word = 'Invoice Number: '.lower()
                            ref_num_extract = pageTxt.partition(split_word)[2].replace(' ', '').partition("invoice")[0]
                            page_num = pdfReader.get_page_number(pageObj)
                            ref_num_match = {
                                'file_path': file_path,
                                'page_num': page_num
                            }
                            master_dict[base_ref_num][ref_num_extract] = ref_num_match
                            # breakpoint()
                            # print('BEFORE BREAK')
                            break
            except Exception as e:  # PyPDF2.errors.PdfReadError:
                print(e)
            pdfFileObj.close()
    return master_dict


def save_json_log(master_dict):
    logs_path = os.path.join(logs_folder_path, 'master_dict_log.txt')
    with open(logs_path, 'w') as master_dict_log:
        master_dict_log.write(json.dumps(master_dict, indent=4))


def search_and_save_locations(base_master_dict) -> dict:
    letter_file_name: str = 'letter.pdf'
    letter_file_path: str = os.path.join(file_folder_path, letter_file_name)
    base_master_dict = process_letters_pdf(letter_file_path, base_master_dict)

    case_file_name: str = 'case.pdf'
    case_file_path: str = os.path.join(file_folder_path, case_file_name)
    base_master_dict = process_case_pdf(case_file_path, base_master_dict)

    base_master_dict = process_location_folder(base_master_dict)

    save_json_log(base_master_dict)

    return base_master_dict


def merge_pdfs(master_dict):
    """
        TODO:
        1. Create PdfFileReader objects for each PDF that was used to extract pages
        2. Iterate through unique master dict and create an output pdf
    """
    file_path = ''
    page_num = ''
    ref_num = ''
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
            # ref_num: str = ref_num_attributes['ref_num']
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

    base_master_list: list = ref_num_list_extract_from_excel_file()
    base_master_dict: dict = create_master_dict(base_master_list)

    print('combining and sorting')
    master_dict = search_and_save_locations(base_master_dict)

    print('merging pdfs')
    merge_pdfs(master_dict)

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
