import configparser
import os
import sys
import math
import json
import PyPDF2
import pandas
from PyPDF2 import PageObject, PdfReader
from datetime import datetime
import PySimpleGUI as Gui
import inspect
import util


def resource_path(relative_path: str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


CONFIG_FOLDER_PATH: str = "Config Files"
LOG_FILE_PATH: str = os.path.join(CONFIG_FOLDER_PATH, r"Scandoc_Imaging_PDF_Merger_log_file.log")
MASTER_DICT_FILE_PATH = os.path.join(CONFIG_FOLDER_PATH, r"master_dict_log.txt")
GUI_CONFIG_PATH: str = os.path.join(CONFIG_FOLDER_PATH, r"gui_config.ini")
OUTPUT_FOLDER_PATH: str = ""
INVOICE_FOLDER_PATH: str = ""
LETTERS_FILE_PATH: str = ""
CASES_FILE_PATH: str = ""
EXCEL_FILE_PATH: str = ""

PROGRAM_FILES_PATH: str = resource_path("Program Files")
SI_LOGO_PATH: str = resource_path(os.path.join(PROGRAM_FILES_PATH, r"si_logo_path.png"))


# with open(os.path.join(r"C:\GitHub-Config-Files\PDF-Matching.json"), 'r', encoding='utf-8') as jsonFile:
#     dict_of_paths: dict = json.load(jsonFile)
# base_folder_path: str = os.path.join(rf"{dict_of_paths.get('base_folder', 'No file folder path found')}")
# invoice_folder_path: str = os.path.join(rf"{dict_of_paths.get('invoice_folder', 'No location folder path found')}")
# output_folder_path: str = os.path.join(rf"{dict_of_paths.get('output_folder', 'No invoice folder path found')}")
# log_folder_path: str = os.path.join(rf"{dict_of_paths.get('log_folder', 'No logs folder path found')}")
# excel_file_path: str = os.path.join(rf"{dict_of_paths.get('excel_file', 'No excel file found')}")
# letter_file_path: str = os.path.join(rf"{dict_of_paths.get('letter_file', 'No letter file path found')}")
# case_file_path: str = os.path.join(rf"{dict_of_paths.get('case_file', 'No case file path found')}")

master_dict: dict = {}
master_list: list = []
read_pages_dict: dict = {}


# def initialize_master_dict():
#     global master_list, master_dict, excel_file_path
#
#     column_name: str = 'Order No'
#     df = pandas.read_excel(excel_file_path)[[column_name]]
#     for i in range(len(df)):
#         if not math.isnan(df[column_name].iloc[i]):
#             master_list.append(str(int(df[column_name].iloc[i])))
#
#     # initialize master_list
#     for ref in master_list:
#         master_dict[ref] = {}
#
#
# def process_letter_pdf():
#     global master_dict, letter_file_path, master_list
#     page: int = 0
#     pdfFileObj = open(letter_file_path, 'rb')
#     try:
#         pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
#         pdfPages: list[PageObject] = pdfReader.pages
#
#         for i in range(len(pdfPages)):
#             pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
#             page_num = pdfReader.get_page_number(pageObj)
#             pageTxt: str = pageObj.extract_text().lower()
#
#             if pageTxt == '' or pageTxt.isspace():
#                 continue
#
#             # if there ever is an issue, I can implement a solution that strips all spaces from pageTxt
#             split_word = 'Ref: '.lower()
#             base_ref_num = pageTxt.partition(split_word)[2].partition("\n")[0].strip()
#
#             # breakpoint()
#
#             if base_ref_num in master_list:
#                 ref_num_match = {
#                     'file_path': letter_file_path,
#                     'page_num': page_num
#                 }
#                 page += 1
#                 ref_num_letter = f'{base_ref_num}-letter-{str(page)}'
#                 master_dict[base_ref_num][ref_num_letter] = ref_num_match
#                 if page == 2:
#                     page = 0
#
#     except Exception as e:  # PyPDF2.errors.PdfReadError:
#         print(f'{e} <- here')
#     pdfFileObj.close()
#
#
# def process_case_pdf():
#     global master_dict, case_file_path, master_list
#     pdfFileObj = open(case_file_path, 'rb')
#     try:
#         pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
#         pdfPages: list[PageObject] = pdfReader.pages
#         for i in range(len(pdfPages)):
#             pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
#             pageTxt: str = pageObj.extract_text().lower()
#
#             if pageTxt == '' or pageTxt.isspace():
#                 continue
#
#             split_word = 'Ref#: '.lower()
#             base_ref_num = pageTxt.partition(split_word)[2].partition(" ")[0].strip()
#             page_num = pdfReader.get_page_number(pageObj)
#
#             # breakpoint()
#
#             if base_ref_num in master_list:
#                 ref_num_match = {
#                     'file_path': case_file_path,
#                     'page_num': page_num
#                 }
#                 ref_num_case = f'{base_ref_num}-case'
#                 master_dict[base_ref_num][ref_num_case] = ref_num_match
#
#     except Exception as e:
#         print(f'{e} <- here')
#     pdfFileObj.close()
#
#
# def process_invoice_folder():
#     global master_dict, master_list
#     for subdir, dirs, files in os.walk(invoice_folder_path):
#         """
#         subdir = current parent folder name
#         dirs = list of directory names in subdir
#         files = list of file names in subdir
#         """
#         for file in files:
#             file_path = os.path.join(subdir, file)
#             root_and_ext = os.path.splitext(file_path)
#             root = root_and_ext[0]
#             ext = root_and_ext[1]
#
#             fileName_and_ext = os.path.splitext(file)
#             fileName = fileName_and_ext[0]
#             fileName_ext = fileName_and_ext[1].lower()
#             complete_filename = ''.join(fileName_and_ext)
#
#             print(f'    Processing File {fileName}...')
#
#             # example
#             # file_path = 'C:\\Users\\samga\\Documents\\Work\\Scandoc-Imaging\\DEMO\\KAMI_FILES\\location_folder\\L1'
#             # file_name_tuple = os.path.splitext(os.path.basename(file_path)) # ('L1', '.pdf')
#
#             # print(file_path)
#
#             pdfFileObj = open(file_path, 'rb')
#             try:
#                 pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
#                 pdfPages: list[PageObject] = pdfReader.pages
#
#                 for i in range(len(pdfPages)):
#                     pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
#                     page_num = pdfReader.get_page_number(pageObj)
#                     pageTxt: str = pageObj.extract_text().lower()
#
#                     if pageTxt == '' or pageTxt.isspace():
#                         continue
#
#                     pageTxt = pageTxt.replace(' ', '')
#
#                     split_word = 'invoicenumber:'.lower()
#                     ref_num_extract = pageTxt.partition(split_word)[2].partition("invoicedate:")[0]
#                     base_num_extract = ref_num_extract.partition('-')[0]
#
#                     # breakpoint()
#
#                     if base_num_extract in master_list:
#                         ref_num_match = {
#                             'file_path': file_path,
#                             'page_num': page_num
#                         }
#
#                         master_dict[base_num_extract][ref_num_extract] = ref_num_match
#
#             except Exception as e:  # PyPDF2.errors.PdfReadError:
#                 print(f'{e} <- here')
#             pdfFileObj.close()
#
#
# def save_json_log():
#     global master_dict
#     logs_path = os.path.join(log_folder_path, 'master_dict_log.txt')
#     with open(logs_path, 'w') as master_dict_log:
#         master_dict_log.write(json.dumps(master_dict, indent=4))
#
#
# def search_and_save_locations():
#     process_letter_pdf()
#     process_case_pdf()
#     process_invoice_folder()
#     save_json_log()
#
#
# def merge_pdfs():
#     global master_dict
#     for base_ref_num, ref_num_matches in master_dict.items():
#         print(f'    Processing {base_ref_num}-Invoices...')
#         pdfOutputPath = os.path.join(output_folder_path, f'{base_ref_num}-Invoices.pdf')
#         pdfOutputFile = open(pdfOutputPath, 'wb')
#         pdfWriter = PyPDF2.PdfWriter()
#
#         # ref_num_keys = list(ref_num_matches.keys())
#         # ref_num_keys.sort()
#         # ref_num_keys = sort_ref_num_list(ref_num_keys)
#         # sorted_ref_num_matches = {key: ref_num_matches[i] for key in ref_num_keys}
#         for ref_num_match, ref_num_attributes in ref_num_matches.items():
#             # file_path = os.path.join(ref_num_attributes['file_path'])
#             file_path = os.path.join(ref_num_attributes.get('file_path', 'No path found'))
#             page_num: str = ref_num_attributes['page_num']
#
#             pdfFileObj = open(file_path, 'rb')
#             try:
#                 pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
#                 pageObj = pdfReader.pages[int(page_num)]
#                 pdfWriter.add_page(pageObj)
#
#                 pdfWriter.write(pdfOutputFile)
#             except Exception as e:  # PyPDF2.errors.PdfReadError:
#                 print(e)
#             pdfFileObj.close()
#         pdfOutputFile.close()


def set_paths_and_save_config_settings(values: dict, config: configparser.ConfigParser):
    """
    This function sets paths from values dictionary to global variables and saves them to
    the gui_config.ini file so that when the user runs the program again, the previously
    chosen paths will populate the input boxes.
    :param values: file paths of previously user chosen folders
    :param config: config object used to update and save file paths to config ini file
    """
    global EXCEL_FILE_PATH, INVOICE_FOLDER_PATH, LETTERS_FILE_PATH, CASES_FILE_PATH, OUTPUT_FOLDER_PATH

    # Create the 'Folders' section if it doesn't exist
    if 'Folders' not in config:
        config['Folders'] = {}

    # set global values and gui config variables to whatever is in the window
    EXCEL_FILE_PATH = config['Folders']['EXCEL_FILE_PATH'] = values["EXCEL_FILE_PATH"]
    INVOICE_FOLDER_PATH = config['Folders']['INVOICE_FOLDER_PATH'] = values["INVOICE_FOLDER_PATH"]
    LETTERS_FILE_PATH = config['Folders']['LETTERS_FILE_PATH'] = values["LETTERS_FILE_PATH"]
    CASES_FILE_PATH = config['Folders']['CASES_FILE_PATH'] = values["CASES_FILE_PATH"]
    OUTPUT_FOLDER_PATH = config['Folders']['OUTPUT_FOLDER_PATH'] = values["OUTPUT_FOLDER_PATH"]

    with open(GUI_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)


def launch_gui():
    global EXCEL_FILE_PATH, INVOICE_FOLDER_PATH, LETTERS_FILE_PATH, CASES_FILE_PATH, OUTPUT_FOLDER_PATH

    gui_config: configparser.ConfigParser = util.load_gui_settings(GUI_CONFIG_PATH)
    window_title: str = gui_config.get('GUI', 'window_title', fallback='')
    font_family: str = gui_config.get('GUI', 'font_family', fallback='')
    font_size: int = int(gui_config.get('GUI', 'font_size', fallback=0))
    theme: str = gui_config.get('GUI', 'theme', fallback='')
    Gui.set_options(font=(font_family, font_size))
    Gui.theme(theme)

    # Retrieve the previously selected folders
    EXCEL_FILE_PATH = gui_config.get('Folders', 'EXCEL_FILE_PATH', fallback='')
    INVOICE_FOLDER_PATH = gui_config.get('Folders', 'INVOICE_FOLDER_PATH', fallback='')
    LETTERS_FILE_PATH = gui_config.get('Folders', 'LETTERS_FILE_PATH', fallback='')
    CASES_FILE_PATH = gui_config.get('Folders', 'CASES_FILE_PATH', fallback='')
    OUTPUT_FOLDER_PATH = gui_config.get('Folders', 'Output_Folder', fallback='')

    file_paths = {
        "Excel File": EXCEL_FILE_PATH,
        "Invoice PDF Folder": INVOICE_FOLDER_PATH,
        "Letters PDF File": LETTERS_FILE_PATH,
        "Cases PDF File": CASES_FILE_PATH,
        "Output Folder": OUTPUT_FOLDER_PATH
    }
    program_title = "Invoice PDF Merger Program"
    layout: list = util.generate_window_layout(SI_LOGO_PATH, program_title, file_paths)

    window: Gui.PySimpleGUI.Window = Gui.Window(window_title, layout)
    while True:
        event: str
        values: dict
        event, values = window.read()

        select_list = []
        try:
            select_list = event.split(' ')
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'split'":
                sys.exit()

        if event in (Gui.WINDOW_CLOSED, "Exit"):
            break
        if 'folder' in select_list and 'open' in select_list:
            print()
            print(f'event = {event}')
            print(f"values = {values}")
            print()

            folder_path = ''
            for k, v in values.items():
                if select_list[0].lower() in k.lower():
                    folder_path = v

            print(f"folder_path = {folder_path}")
            if folder_path == '':
                Gui.popup_error("Please Select a Valid Folder First.")
            else:
                # util.open_folder_explorer(values[folder_name])
                util.open_folder_explorer(folder_path)
                # breakpoint()
        if event == "Generate PDF Files":
            if util.is_valid_path(values["Employee_Excel_Timesheets_Folder"]) and \
                    util.is_valid_path(values["Signed_Employee_Blank_PDFs_Folder"]) and \
                    util.is_valid_path(values["Output_Folder"]):
                set_paths_and_save_config_settings(values, gui_config)
                breakpoint()


def run_script():
    start_time = datetime.now()

    # print('\nLoading Excel File...')
    # initialize_master_dict()
    # print('Done!')
    #
    # print('\nSearching PDFs...')
    # search_and_save_locations()
    # print('Done!')
    #
    # print('\nCreating New PDFs...')
    # merge_pdfs()
    # print('Done!')
    #
    # end_time = datetime.now()
    # run_time = end_time - start_time
    # print('\nProgram Run Time:', run_time)
