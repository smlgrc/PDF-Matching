from datetime import datetime
import os
import random

import PyPDF2
from PyPDF2 import PageObject, PdfReader
from fpdf import FPDF

prefix_list: list[str] = ['24', '25']
ext_list: list[str] = ['1', '2', '3', '4', '5', '6', '7', '8']

ref_num_24: list[str] = ['241442', '241996', '242136', '243223', '243977', '244459', '244860', '247155', '248947', '248975']
ref_num_25: list[str] = ['251591', '251656', '251891', '252316', '252777', '253207', '254770', '256442', '256703', '256853']

unique_master_list: list[str] = ['241442', '241996', '242136', '243223', '243977', '244459', '244860', '247155', '248947', '248975',
                                 '251591', '251656', '251891', '252316', '252777', '253207', '254770', '256442', '256703', '256853']

unique_master_dict: dict = {'241442': [], '241996': [], '242136': [], '243223': [], '243977': [], '244459': [], '244860': [], '247155': [], '248947': [], '248975': [],
                            '251591': [], '251656': [], '251891': [], '252316': [], '252777': [], '253207': [], '254770': [], '256442': [], '256703': [], '256853': []}

list_24_1 = ['248975-1', '243223-1', '247155-1', '241996-1', '244860-1', '241442-1', '243977-1', '244459-1', '248947-1', '242136-1']
list_24_2 = ['241996-2', '244459-2', '247155-2', '243223-2', '244860-2', '242136-2', '248975-2', '241442-2', '243977-2', '248947-2']
list_24_4 = ['243223-4', '247155-4', '244459-4', '242136-4', '248975-4', '241442-4', '244860-4', '248947-4', '241996-4', '243977-4']

list_25_1 = ['251891-1', '254770-1', '251591-1', '253207-1', '252316-1', '251656-1', '252777-1', '256703-1', '256853-1', '256442-1']
list_25_2 = ['252316-2', '256703-2', '253207-2', '256853-2', '252777-2', '251591-2', '254770-2', '251891-2', '256442-2', '251656-2']
list_25_4 = ['256442-4', '254770-4', '256703-4', '251891-4', '252316-4', '256853-4', '253207-4', '251656-4', '251591-4', '252777-4']

master_list = ['248975-1', '243223-1', '247155-1', '241996-1', '244860-1', '241442-1', '243977-1', '244459-1', '248947-1', '242136-1', '241996-2', '244459-2', '247155-2', '243223-2', '244860-2', '242136-2', '248975-2', '241442-2', '243977-2', '248947-2', '243223-4', '247155-4', '244459-4', '242136-4', '248975-4', '241442-4', '244860-4', '248947-4', '241996-4', '243977-4', '251891-1', '254770-1', '251591-1', '253207-1', '252316-1', '251656-1', '252777-1', '256703-1', '256853-1', '256442-1', '252316-2', '256703-2', '253207-2', '256853-2', '252777-2', '251591-2', '254770-2', '251891-2', '256442-2', '251656-2', '256442-4', '254770-4', '256703-4', '251891-4', '252316-4', '256853-4', '253207-4', '251656-4', '251591-4', '252777-4']
sorted_master_list = ['241442-1', '241442-2', '241442-4', '241996-1', '241996-2', '241996-4', '242136-1', '242136-2', '242136-4', '243223-1', '243223-2', '243223-4', '243977-1', '243977-2', '243977-4', '244459-1', '244459-2', '244459-4', '244860-1', '244860-2', '244860-4', '247155-1', '247155-2', '247155-4', '248947-1', '248947-2', '248947-4', '248975-1', '248975-2', '248975-4', '251591-1', '251591-2', '251591-4', '251656-1', '251656-2', '251656-4', '251891-1', '251891-2', '251891-4', '252316-1', '252316-2', '252316-4', '252777-1', '252777-2', '252777-4', '253207-1', '253207-2', '253207-4', '254770-1', '254770-2', '254770-4', '256442-1', '256442-2', '256442-4', '256703-1', '256703-2', '256703-4', '256853-1', '256853-2', '256853-4']

ref_file_path: str = r'C:\Users\samga\Documents\GitHub\PDF-Matching\PDFs'
output_path: str = r'C:\Users\samga\Documents\GitHub\PDF-Matching\PDFs\Reference-Number-Invoices'


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
        for match_dict in ref_num_matches:
            file_path = os.path.join(match_dict['file_path'])
            field_num: str = match_dict['field_num']
            page_num: str = match_dict['page_num']

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
    pdf_file_path: str = rf"C:\Users\samga\Documents\GitHub\PDF-Matching\PDFs\location-{prefix}-{ext}.pdf"
    output_path = os.path.join(pdf_file_path)
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


def combine_and_sort(base_master_dict, base_master_list):
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
                        if ref_num in pageTxt:
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
                                    base_master_dict[key].append(ref_num_match)
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

    iterations = 2

    ref_base_list_24 = generate_random_ref_num_list('24', iterations)
    ref_base_list_25 = generate_random_ref_num_list('25', iterations)

    ref_list_24 = shuffle_and_add_location_ext(ref_base_list_24)
    ref_list_25 = shuffle_and_add_location_ext(ref_base_list_25)

    for ext in ext_list:
        create_pdf(ref_list_24, '24', ext)
    for ext in ext_list:
        create_pdf(ref_list_25, '25', ext)

    base_master_dict = {}
    for ref in ref_base_list_24:
        base_master_dict[str(ref)] = []
    for ref in ref_base_list_25:
        base_master_dict[str(ref)] = []

    base_master_list = []
    for ref in ref_list_24:
        base_master_list.append(ref)
    for ref in ref_list_25:
        base_master_list.append(ref)

    master_dict = combine_and_sort(base_master_dict, base_master_list)

    merge_pdfs(master_dict)

    # test()
    end_time = datetime.now()

    run_time = end_time - start_time
    print('\nProgram Run Time:', run_time)

    # breakpoint()


if __name__ == '__main__':
    main()
