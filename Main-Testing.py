import re
from datetime import datetime
import os
import random

import PyPDF2
from PyPDF2 import PageObject, PdfReader
from fpdf import FPDF

#  500 takes -> Program Run Time: 0:06:30.022575
# 1080 takes -> Program Run Time: 0:30:31.011427
# 1200 takes -> Program Run Time: 0:37:31.029105

iterations = 500
prefix_list: list[str] = ['24', '25']
ext_list: list[str] = ['1', '2', '3', '4', '5', '6', '7', '8', '9a', '9b', '16', '16a']
ref_file_path: str = os.path.join(r'PATH-TO-KAMI-FILES')
output_path: str = os.path.join(r'PATH-TO-INVOICE-FOLDER')


def generate_random_base_ref_num_list(prefix: str, iterations: int) -> list[int]:
    '''
    :param prefix: '24' + '1234' = '241234'
    :param iterations: number of iterations
    :return: retuns a list of randomly generated unique reference numbers
    '''
    start: int = 1000
    end: int = 9999

    ref_num_list: list[int] = []
    rand_num_list: list[int] = []
    rand_num: int = random.randint(start, end)

    for num in range(iterations):
        while rand_num in rand_num_list:
            rand_num = random.randint(start, end)

        rand_num_list.append(rand_num)

        ref_str: str = prefix + str(rand_num)
        ref_num: int = int(ref_str)
        ref_num_list.append(ref_num)

    ref_num_list.sort()

    return ref_num_list


def shuffle_and_add_location_to_base_list(ref_num_list) -> list[str]:
    ref: list[str] = []

    for ext in ext_list:
        random.shuffle(ref_num_list)
        for i in range(len(ref_num_list)):
            ref.append(str(ref_num_list[i]) + '-' + ext)

    return ref


def create_pdf(ref_num_list: list, prefix: str, ext: str):
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    for ref_num in ref_num_list:
        if ref_num.endswith(f'-{ext}'):
            # Add a page
            pdf.add_page()

            # set style and size of font
            # that you want in the pdf
            pdf.set_font("Arial", size=15)

            # add another cell
            pdf.cell(200, 10, txt="Scandoc Imaging.",
                     ln=2, align='L')

            # create a cell
            pdf.cell(175, 10, txt=f'Ref: {ref_num}',
                     ln=1, align='R')

            # add another cell
            pdf.cell(200, 10, txt="Invoice information.",
                     ln=2, align='L')

    pdf_output_path = os.path.join(ref_file_path, rf'location-{prefix}-{ext}.pdf')
    pdf.output(pdf_output_path)


def sort_ref_num_list(ref_num_list):
    location_list = []
    for ref_num in ref_num_list:
        location_parts = re.findall(r'\d+', ref_num.partition('-')[2])
        location = ''.join(location_parts)
        location_list.append(int(location))

    new_location_list, new_ref_num_list = zip(*sorted(zip(location_list, ref_num_list)))
    new_ref_num_list = list(new_ref_num_list)
    return new_ref_num_list


def search_and_save_locations(base_master_dict):
    for subdir, dirs, files in os.walk(ref_file_path):
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
                    pageTxt: str = pageObj.extract_text()
                    # print(f'\n\nOUTER INDEX = {i}\n\n')

                    # breakpoint()
                    for j, base_ref_num in enumerate(list(base_master_dict.keys())):
                        # print(f'\nbase ref num = {base_ref_num}')
                        # print('PAGE TEXT')
                        # print(pageTxt)
                        # print(f'\n\nINNER INDEX = {j}\n\n')
                        if base_ref_num in pageTxt:
                            split_word = 'Ref: '
                            ref_num_extract = pageTxt.partition(split_word)[2].partition("\n")[0]
                            page_num = pdfReader.get_page_number(pageObj)
                            ref_num_match = {
                                'file_path': file_path,
                                'page_num': page_num
                            }
                            base_master_dict[base_ref_num][ref_num_extract] = ref_num_match
                            # print('\n\nBREAKING\n\n')
                            break

                    # # for j, ref_num in enumerate(sorted_master_list):
                    # for j, ref_num in enumerate(base_master_list):
                    #     ref_num_new_line = f'{ref_num}\n'
                    #     if ref_num_new_line in pageTxt:
                    #         for key in base_master_dict.keys():
                    #             if key in pageTxt:
                    #                 # breakpoint()
                    #                 split_word = 'Ref: '
                    #                 ref_num_extract = pageTxt.partition(split_word)[2].partition("\n")[0]
                    #                 page_num = pdfReader.get_page_number(pageObj)
                    #                 ref_num_match = {
                    #                     # 'ref_num': ref_num_extract,
                    #                     'file_path': file_path,
                    #                     'page_num': page_num
                    #                 }
                    #                 base_master_dict[key][ref_num_extract] = ref_num_match
            except Exception as e:  # PyPDF2.errors.PdfReadError:
                print(e)
            pdfFileObj.close()
    return base_master_dict


def search_and_save_locations_OLD(base_master_dict, base_master_list):
    for subdir, dirs, files in os.walk(ref_file_path):
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
                    pageTxt: str = pageObj.extract_text()

                    # for j, ref_num in enumerate(sorted_master_list):
                    for j, ref_num in enumerate(base_master_list):
                        ref_num_new_line = f'{ref_num}\n'
                        if ref_num_new_line in pageTxt:
                            for key in base_master_dict.keys():
                                if key in pageTxt:
                                    # breakpoint()
                                    split_word = 'Ref: '
                                    ref_num_extract = pageTxt.partition(split_word)[2].partition("\n")[0]
                                    page_num = pdfReader.get_page_number(pageObj)
                                    ref_num_match = {
                                        # 'ref_num': ref_num_extract,
                                        'file_path': file_path,
                                        'page_num': page_num
                                    }
                                    base_master_dict[key][ref_num_extract] = ref_num_match

            except Exception as e:  # PyPDF2.errors.PdfReadError:
                print(e)
            pdfFileObj.close()
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
        pdfOutputPath = os.path.join(output_path, f'{base_ref_num}-invoices.pdf')
        pdfOutputFile = open(pdfOutputPath, 'wb')
        pdfWriter = PyPDF2.PdfWriter()

        ref_num_keys = list(ref_num_matches.keys())
        ref_num_keys.sort()
        ref_num_keys = sort_ref_num_list(ref_num_keys)
        sorted_ref_num_matches = {i: ref_num_matches[i] for i in ref_num_keys}
        for ref_num_match, ref_num_attributes in sorted_ref_num_matches.items():
            file_path = os.path.join(ref_num_attributes['file_path'])
            # ref_num: str = ref_num_attributes['ref_num']
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


def print_lists(list1, list2):
    for i in list1:
        print(i)
    print()
    for i in list2:
        print(i)


def demo():
    start_time = datetime.now()

    print('generating random reference numbers')
    ref_base_list_24: list = generate_random_base_ref_num_list('24', iterations)
    ref_base_list_25: list = generate_random_base_ref_num_list('25', iterations)
    print_lists(ref_base_list_24, ref_base_list_25)
    breakpoint()

    print('shuffling and adding location to base reference numbers')
    ref_list_24: list = shuffle_and_add_location_to_base_list(ref_base_list_24)
    ref_list_25: list = shuffle_and_add_location_to_base_list(ref_base_list_25)
    print_lists(ref_list_24, ref_list_25)
    breakpoint()

    print('creating pdfs')
    for ext in ext_list:
        create_pdf(ref_list_24, '24', ext)
    for ext in ext_list:
        create_pdf(ref_list_25, '25', ext)
    breakpoint()

    print('creating base master dictionary')
    base_master_dict = {}
    for ref in ref_base_list_24:
        base_master_dict[str(ref)] = {}
    for ref in ref_base_list_25:
        base_master_dict[str(ref)] = {}
    breakpoint()

    print('creating base master list')
    base_master_list = []
    for ref in ref_list_24:
        base_master_list.append(ref)
    for ref in ref_list_25:
        base_master_list.append(ref)
    breakpoint()

    print('combining and sorting')
    master_dict = search_and_save_locations(base_master_dict)#, base_master_list)
    print(f'\nExample for -> {list(master_dict.keys())[0]}\n')
    for k, v in master_dict[list(master_dict.keys())[0]].items():
        print(k, v)
    breakpoint()

    print('merging pdfs')
    merge_pdfs(master_dict)

    end_time = datetime.now()
    run_time = end_time - start_time
    print('\nProgram Run Time:', run_time)


def run_script():
    start_time = datetime.now()

    print('generating random reference numbers')
    ref_base_list_24: list = generate_random_base_ref_num_list('24', iterations)
    ref_base_list_25: list = generate_random_base_ref_num_list('25', iterations)

    print('shuffling and adding location to base reference numbers')
    ref_list_24: list = shuffle_and_add_location_to_base_list(ref_base_list_24)
    ref_list_25: list = shuffle_and_add_location_to_base_list(ref_base_list_25)

    print('creating pdfs')
    for ext in ext_list:
        create_pdf(ref_list_24, '24', ext)
    for ext in ext_list:
        create_pdf(ref_list_25, '25', ext)

    print('creating base master dictionary')
    base_master_dict = {}
    for ref in ref_base_list_24:
        base_master_dict[str(ref)] = {}
    for ref in ref_base_list_25:
        base_master_dict[str(ref)] = {}

    # print('creating base master list')
    # base_master_list = []
    # for ref in ref_list_24:
    #     base_master_list.append(ref)
    # for ref in ref_list_25:
    #     base_master_list.append(ref)

    print('combining and sorting')
    master_dict = search_and_save_locations(base_master_dict)#, base_master_list)

    print('merging pdfs')
    merge_pdfs(master_dict)

    end_time = datetime.now()
    run_time = end_time - start_time
    print('\nProgram Run Time:', run_time)


def main():
    # demo()
    run_script()


if __name__ == '__main__':
    main()
