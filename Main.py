import os
import random
from fpdf import FPDF

prefix_list: list[str] = ['24', '25']
ext_list: list[str] = ['1', '2', '4']

ref_num_24: list[str] = ['241442', '241996', '242136', '243223', '243977', '244459', '244860', '247155', '248947', '248975']
ref_num_25: list[str] = ['251591', '251656', '251891', '252316', '252777', '253207', '254770', '256442', '256703', '256853']

list_24_1 = ['248975-1', '243223-1', '247155-1', '241996-1', '244860-1', '241442-1', '243977-1', '244459-1', '248947-1', '242136-1']
list_24_2 = ['241996-2', '244459-2', '247155-2', '243223-2', '244860-2', '242136-2', '248975-2', '241442-2', '243977-2', '248947-2']
list_24_4 = ['243223-4', '247155-4', '244459-4', '242136-4', '248975-4', '241442-4', '244860-4', '248947-4', '241996-4', '243977-4']

list_25_1 = ['251891-1', '254770-1', '251591-1', '253207-1', '252316-1', '251656-1', '252777-1', '256703-1', '256853-1', '256442-1']
list_25_2 = ['252316-2', '256703-2', '253207-2', '256853-2', '252777-2', '251591-2', '254770-2', '251891-2', '256442-2', '251656-2']
list_25_4 = ['256442-4', '254770-4', '256703-4', '251891-4', '252316-4', '256853-4', '253207-4', '251656-4', '251591-4', '252777-4']


def create_pdf(ref_num_list: list, prefix: str, ext: str):
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    for ref_num in ref_num_list:
        # Add a page
        pdf.add_page()

        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Arial", size=15)

        # create a cell
        pdf.cell(200, 10, txt=ref_num,
                 ln=1, align='C')

        # # add another cell
        # pdf.cell(200, 10, txt="A Computer Science portal for geeks.",
        #          ln=2, align='C')

    # save the pdf with name .pdf
    file_path: str = rf"C:\Users\samga\Documents\GitHub\PDF-Matching\PDFs\location-{prefix}-{ext}.pdf"
    output_path = os.path.join(file_path)
    pdf.output(output_path)


def shuffle_and_add_location_ext():# -> list[str]:
    ref1: list[str] = []
    ref2: list[str] = []

    for ext in ext_list:
        random.shuffle(ref_num_24)
        random.shuffle(ref_num_25)
        for i in range(10):
            ref1.append(ref_num_24[i] + '-' + ext)
            ref2.append(ref_num_25[i] + '-' + ext)

    print(ref1)
    print(ref2)


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


def print_ref_num_list():
    print(ref_num_24)
    print(ref_num_25)


def sort_and_combine():
    pass


def main():
    # print_ref_num_list()
    # shuffle_and_add_location_ext()
    sort_and_combine()


if __name__ == '__main__':
    main()
