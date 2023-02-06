import re
from datetime import datetime
import os
import random

import PyPDF2
from PyPDF2 import PageObject, PdfReader
from fpdf import FPDF

iterations = 500  # 1080 takes -> Program Run Time:0:30:31.011427
prefix_list: list[str] = ['24', '25']
ext_list: list[str] = ['1', '2', '3', '4', '5', '6', '7', '8', '9a', '9b', '16', '16a']
ref_file_path: str = r'C:\Users\samga\Documents\Work\Scandoc-Imaging\PDFs'
output_path: str = r'C:\Users\samga\Documents\Work\Scandoc-Imaging\PDFs\Reference-Number-Invoices'


def sort_ref_num_list(ref_num_list):
    location_list = []
    for ref_num in ref_num_list:
        location_parts = re.findall(r'\d+', ref_num.partition('-')[2])
        location = ''.join(location_parts)
        location_list.append(int(location))

    new_location_list, new_ref_num_list = zip(*sorted(zip(location_list, ref_num_list)))
    new_ref_num_list = list(new_ref_num_list)
    return new_ref_num_list


def merge_pdfs(master_dict):
    """
        TODO:
        1. Create PdfFileReader objects for each PDF that was used to extract pages
        2. Iterate through unique master dict and create an output pdf
    """
    for base_ref_num, ref_num_matches in master_dict.items():
        print(f'Processing {base_ref_num}...')
        pdfOutputPath = os.path.join(output_path, f'{base_ref_num}-invoices.pdf')
        pdfOutputFile = open(pdfOutputPath, 'wb')
        pdfWriter = PyPDF2.PdfWriter()

        # for match_dict in ref_num_matches:
        ref_num_keys = list(ref_num_matches.keys())
        ref_num_keys.sort()
        ref_num_keys = sort_ref_num_list(ref_num_keys)
        sorted_ref_num_matches = {i: ref_num_matches[i] for i in ref_num_keys}
        # breakpoint()
        for ref_num, ref_num_attributes in sorted_ref_num_matches.items():
            file_path = os.path.join(ref_num_attributes['file_path'])
            field_num: str = ref_num_attributes['field_num']
            page_num: str = ref_num_attributes['page_num']

            # with open(file_path, 'rb') as pdfFileObj:
            pdfFileObj = open(file_path, 'rb')
            try:
                pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
                pageObj = pdfReader.pages[int(page_num)]
                pdfWriter.add_page(pageObj)

                # pdfOutputFile = open(pdfOutputPath, 'wb')
                pdfWriter.write(pdfOutputFile)
                # with open(pdfOutputPath, 'wb') as pdfOutputFile:
                #     pdfWriter.write(pdfOutputFile)

            except Exception as e:  # PyPDF2.errors.PdfReadError:
                print(e)
            pdfFileObj.close()
        pdfOutputFile.close()

        # breakpoint()


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
            pdf.cell(200, 10, txt="Extra text here.",
                     ln=2, align='L')

    # save the pdf with name .pdf
    # pdf_file_path: str = rf"C:\Users\samga\Documents\GitHub\PDF-Matching\PDFs\location-{prefix}-{ext}.pdf"
    # output_path = os.path.join(pdf_file_path)
    output_path = os.path.join(ref_file_path, rf'location-{prefix}-{ext}.pdf')
    pdf.output(output_path)


def shuffle_and_add_location_ext(ref_num_list) -> list[str]:
    ref: list[str] = []

    for ext in ext_list:
        random.shuffle(ref_num_list)
        for i in range(len(ref_num_list)):
            ref.append(str(ref_num_list[i]) + '-' + ext)

    # for ref_num in ref:
    #     print(ref_num)
    return ref


def generate_random_ref_num_list(prefix: str, iterations: int) -> list[int]:
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


def search_and_save_locations(base_master_dict, base_master_list):
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
                # print('Number of PDF pages = ' + str(len(pdfReader.pages)))

                pdfPages: list[PageObject] = pdfReader.pages

                # print('\n=== Page Extracts ===')
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
                                    field_num = pageTxt.partition(split_word)[2].partition("\n")[0]
                                    page_num = pdfReader.get_page_number(pageObj)
                                    ref_num_match = {
                                        'file_path': file_path,
                                        'field_num': field_num,
                                        'page_num': page_num
                                    }
                                    # base_master_dict[key].append(ref_num_match)
                                    base_master_dict[key][ref_num] = ref_num_match

                                    # for k,v in base_master_dict.items(): print(k, v)
                                    # breakpoint()
                                    # print('whatever')

            except Exception as e:  # PyPDF2.errors.PdfReadError:
                print(e)
            pdfFileObj.close()
    return base_master_dict

    # for k,v in unique_master_dict.items():
    #     print()
    #     print(f'key = {k}')
    #     print(f'value = {v}')
        # for dictionary in v:
        #     for k2, v2 in dictionary:
        #         print(f'key2 = {k2}')
        #         print(f'value2 = {v2}')


def test():
    my_string = 'Scandoc Imaging.\nRef: 248975-1\nExtra text here.'#"Python is one of the most popular programming languages"

    split_word = 'Ref: '

    print("Original string: " + str(my_string))

    print("Split string: " + str(split_word))

    res_str = my_string.partition(split_word)[2].partition("\n")[0]
    # breakpoint()
    # new_str = res_str.partition("\n")[0]

    print("String result after the occurrence substring: " + res_str)


def main():
    start_time = datetime.now()

    print('generating random reference numbers')
    ref_base_list_24 = generate_random_ref_num_list('24', iterations)
    ref_base_list_25 = generate_random_ref_num_list('25', iterations)

    print('shuffling and adding location to base reference numbers')
    ref_list_24 = shuffle_and_add_location_ext(ref_base_list_24)
    ref_list_25 = shuffle_and_add_location_ext(ref_base_list_25)

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

    print('creating base master list')
    base_master_list = []
    for ref in ref_list_24:
        base_master_list.append(ref)
    for ref in ref_list_25:
        base_master_list.append(ref)

    print('combining and sorting')
    master_dict = search_and_save_locations(base_master_dict, base_master_list)
    print('merging pdfs')
    merge_pdfs(master_dict)

    end_time = datetime.now()
    run_time = end_time - start_time
    print('\nProgram Run Time:', run_time)


if __name__ == '__main__':
    main()
