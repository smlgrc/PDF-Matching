import configparser
import copy
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
from util import FileSystemObject as FSO


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

DEFENSE: FSO = FSO("Defense PDF File", "", "DEFENSE_FILE_PATH", "File", {"name": "Defense", "abbreviation": "Def Notice"}, {})
INSURANCE: FSO = FSO("Insurance PDF File", "", "INSURANCE_FILE_PATH", "File", {"name": "Insurance", "abbreviation": "Ins Notice"}, {})
EXCEL: FSO = FSO("Reference Number Excel File", "", "EXCEL_FILE_PATH", "File", None, None)
SUBPOENA: FSO = FSO("Subpoena PDF Folder", "", "SUBPOENA_FOLDER_PATH", "Folder", None, None)
OUTPUT: FSO = FSO("Output Folder", "", "OUTPUT_FOLDER_PATH", "Folder", None, None)

MASTER_DEFENSE_DICT: dict = {}
MASTER_INSURANCE_DICT: dict = {}
PROJECT_OBJECTS: list[FSO] = [DEFENSE, INSURANCE, EXCEL, SUBPOENA, OUTPUT]
JOB_LIST: list[FSO] = [DEFENSE, INSURANCE]

PROGRAM_FILES_PATH: str = resource_path("Program Files")
SI_LOGO_PATH: str = resource_path(os.path.join(PROGRAM_FILES_PATH, r"si_logo_path.png"))

MASTER_DICT: dict = {}
MASTER_LIST: list = []
READ_PAGES_DICT: dict = {}


def initialize_master_dicts():
    global MASTER_DICT, MASTER_LIST, JOB_LIST

    column_name: str = 'Order No'
    df = pandas.read_excel(EXCEL.get_field_path())[[column_name]]
    for i in range(len(df)):
        if not math.isnan(df[column_name].iloc[i]):
            MASTER_LIST.append(str(int(df[column_name].iloc[i])))

    # initialize master_list
    for ref in MASTER_LIST:
        MASTER_DICT[ref] = {}

    for job in JOB_LIST:
        job.set_master_dict(copy.deepcopy(MASTER_DICT))


def process_sdt_pdfs():
    global JOB_LIST
    for subdir, dirs, files in os.walk(SUBPOENA.get_field_path()):
        """
        subdir = current parent folder name
        dirs = list of directory names in subdir
        files = list of file names in subdir
        """
        for file in sorted(files):
            file_path = os.path.join(subdir, file)
            root_and_ext = os.path.splitext(file_path)
            root = root_and_ext[0]
            ext = root_and_ext[1]
            base_ref = ''

            fileName_and_ext = os.path.splitext(file)
            fileName = fileName_and_ext[0]
            fileName_ext = fileName_and_ext[1].lower()
            complete_filename = ''.join(fileName_and_ext)

            for ref in MASTER_LIST:
                if ref in os.path.basename(subdir):
                    base_ref = ref
                    break

            pdfFileObj = open(file_path, 'rb')
            pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
            pdfPages: list[PageObject] = pdfReader.pages
            for i in range(len(pdfPages)):
                ref_num_match = {
                    'file_path': file_path,
                    'page_num': i
                }
                for job in JOB_LIST:
                    job.get_master_dict()[base_ref][f'{base_ref}-{fileName} page {i + 1}'] = ref_num_match
            print()
            print(base_ref)
            print(subdir, file)
            print()
            print(DEFENSE.get_master_dict())
            print()
            print(INSURANCE.get_master_dict())
            print()
            breakpoint()

            print(f'    Processing File {fileName}...')

            # example
            # file_path = 'C:\\Users\\samga\\Documents\\Work\\Scandoc-Imaging\\DEMO\\KAMI_FILES\\location_folder\\L1'
            # file_name_tuple = os.path.splitext(os.path.basename(file_path)) # ('L1', '.pdf')


def process_job_pdfs(job: FSO):
    global MASTER_DICT, MASTER_LIST, JOB_LIST
    page: int = 0
    current_base_ref_num: str = ""
    pdfFileObj = open(job.get_field_path(), 'rb')
    try:
        pdfReader: PdfReader = PdfReader(pdfFileObj, strict=False)
        pdfPages: list[PageObject] = pdfReader.pages

        for i in range(len(pdfPages)):
            pageObj: PyPDF2._page.PageObject = pdfReader.pages[i]
            page_num = pdfReader.get_page_number(pageObj)

            pageTxt: str = pageObj.extract_text().lower()

            # if page_num == 1:
            #     breakpoint()

            if pageTxt == '' or pageTxt.isspace():
                continue
            # if there ever is an issue, I can implement a solution that strips all spaces from pageTxt
            split_word = 'Ref#:'.lower()

            base_ref_num = pageTxt.replace(" ", "").partition(split_word)[2].partition("\n")[0].strip()
            if base_ref_num:
                current_base_ref_num = base_ref_num

            if current_base_ref_num in MASTER_LIST:
                ref_num_match = {
                    'file_path': job.get_field_path(),
                    'page_num': page_num
                }
                page += 1
                ref_num_job = f'{current_base_ref_num}_{job.get_job_attributes()["abbreviation"].replace(" ", "_")}_{str(page)}'

                job.get_master_dict()[current_base_ref_num][ref_num_job] = ref_num_match
                # MASTER_DICT[current_base_ref_num][ref_num_job] = ref_num_match
                if page == 2:
                    page = 0

    except Exception as e:  # PyPDF2.errors.PdfReadError:
        print(f'{e} <- here')
    pdfFileObj.close()

    print()
    for k, v in MASTER_DICT.items(): print(k, v)


# def process_case_pdf():
#     global MASTER_DICT, MASTER_LIST
#     pdfFileObj = open(CASES.get_field_path(), 'rb')
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
#             if base_ref_num in MASTER_LIST:
#                 ref_num_match = {
#                     'file_path': CASES.get_field_path(),
#                     'page_num': page_num
#                 }
#                 ref_num_case = f'{base_ref_num}-case'
#                 MASTER_DICT[base_ref_num][ref_num_case] = ref_num_match
#     except Exception as e:
#         print(f'{e} <- here')
#     pdfFileObj.close()


# def process_invoice_folder():
#     global MASTER_DICT, MASTER_LIST
#     for subdir, dirs, files in os.walk(INVOICE.get_field_path()):
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
#                     if base_num_extract in MASTER_LIST:
#                         ref_num_match = {
#                             'file_path': file_path,
#                             'page_num': page_num
#                         }
#
#                         MASTER_DICT[base_num_extract][ref_num_extract] = ref_num_match
#
#             except Exception as e:  # PyPDF2.errors.PdfReadError:
#                 print(f'{e} <- here')
#             pdfFileObj.close()


def save_json_log():
    with open(MASTER_DICT_FILE_PATH, 'w') as master_dict_log:
        master_dict_log.write(json.dumps(MASTER_DICT, indent=4))


def merge_pdfs():
    global MASTER_DICT
    for base_ref_num, ref_num_matches in MASTER_DICT.items():
        print(f'    Processing {base_ref_num}-Invoices...')
        pdfOutputPath = os.path.join(OUTPUT.get_field_path(), f'{base_ref_num}-Invoices.pdf')
        pdfOutputFile = open(pdfOutputPath, 'wb')
        pdfWriter = PyPDF2.PdfWriter()

        # ref_num_keys = list(ref_num_matches.keys())
        # ref_num_keys.sort()
        # ref_num_keys = sort_ref_num_list(ref_num_keys)
        # sorted_ref_num_matches = {key: ref_num_matches[i] for key in ref_num_keys}
        for ref_num_match, ref_num_attributes in ref_num_matches.items():
            # file_path = os.path.join(ref_num_attributes['file_path'])
            file_path = os.path.join(ref_num_attributes.get('file_path', 'No path found'))
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


def set_paths_and_save_config_settings(values: dict, config: configparser.ConfigParser):
    """
    This function sets paths from values dictionary to global variables and saves them to
    the gui_config.ini file so that when the user runs the program again, the previously
    chosen paths will populate the input boxes.
    :param values: file paths of previously user chosen folders
    :param config: config object used to update and save file paths to config ini file
    """
    global PROJECT_OBJECTS

    # Create the 'Folders' section if it doesn't exist
    if 'Folders' not in config:
        config['Folders'] = {}

    # set global values and gui config variables to whatever is in the window
    for object in PROJECT_OBJECTS:
        file_path: str = values[object.get_field_name()]
        object.set_field_path(file_path)
        config['Folders'][object.get_field_path_name()] = file_path

    with open(GUI_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)


def launch_gui():
    global PROJECT_OBJECTS

    gui_config: configparser.ConfigParser = util.load_gui_settings(GUI_CONFIG_PATH)
    window_title: str = 'Defense and Insurance PDF Merger'
    font_family: str = gui_config.get('GUI', 'font_family', fallback='')
    font_size: int = int(gui_config.get('GUI', 'font_size', fallback=0))
    theme: str = gui_config.get('GUI', 'theme', fallback='SystemDefault')
    Gui.set_options(font=(font_family, font_size))
    Gui.theme(theme)

    # Retrieve the previously selected folders
    for object in PROJECT_OBJECTS:
        object.set_field_path(gui_config.get('Folders', object.get_field_path_name(), fallback=''))

    program_title = "Defense and Insurance PDF Merger"
    layout: list = util.generate_window_layout(SI_LOGO_PATH, program_title, PROJECT_OBJECTS)

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
            folder_path = ''
            for k, v in values.items():
                if select_list[0].lower() in k.lower():
                    folder_path = v
            if folder_path == '':
                Gui.popup_error("Please Select a Valid Folder First.")
            else:
                util.open_folder_explorer(folder_path)
        if event == "Generate PDF Files":
            if util.verify_paths(values, PROJECT_OBJECTS):
                set_paths_and_save_config_settings(values, gui_config)
                run_script(window)
            else:
                Gui.popup_error("Missing or Invalid Filepath(s)\nPlease check that you've selected all folders")


def search_and_save_locations():
    for job in JOB_LIST:
        process_job_pdfs(job)

    # TODO: PROCESS SUBPOENAS INSTEAD OF RUNNING JOB TWICE, JUST ADD THE REST OF THE FILES TO EACH DICT
    # 260767
    # {'260767_Ins_Notice_1': {
    #     'file_path': 'C:/Users/Sam/Documents/Personal/Work/Scandoc Imaging/Defense and Insurance Folder/Ins Notice.pdf',
    #     'page_num': 0}, '260767_Ins_Notice_2': {
    #     'file_path': 'C:/Users/Sam/Documents/Personal/Work/Scandoc Imaging/Defense and Insurance Folder/Ins Notice.pdf',
    #     'page_num': 1}}
    # 260768
    # {'260768_Ins_Notice_1': {
    #     'file_path': 'C:/Users/Sam/Documents/Personal/Work/Scandoc Imaging/Defense and Insurance Folder/Ins Notice.pdf',
    #     'page_num': 2}, '260768_Ins_Notice_2': {
    #     'file_path': 'C:/Users/Sam/Documents/Personal/Work/Scandoc Imaging/Defense and Insurance Folder/Ins Notice.pdf',
    #     'page_num': 3}}
    # 260769
    # {'260769_Ins_Notice_1': {
    #     'file_path': 'C:/Users/Sam/Documents/Personal/Work/Scandoc Imaging/Defense and Insurance Folder/Ins Notice.pdf',
    #     'page_num': 4}, '260769_Ins_Notice_2': {
    #     'file_path': 'C:/Users/Sam/Documents/Personal/Work/Scandoc Imaging/Defense and Insurance Folder/Ins Notice.pdf',
    #     'page_num': 5}}
    # 260770
    # {'260770_Ins_Notice_1': {
    #     'file_path': 'C:/Users/Sam/Documents/Personal/Work/Scandoc Imaging/Defense and Insurance Folder/Ins Notice.pdf',
    #     'page_num': 6}, '260770_Ins_Notice_2': {
    #     'file_path': 'C:/Users/Sam/Documents/Personal/Work/Scandoc Imaging/Defense and Insurance Folder/Ins Notice.pdf',
    #     'page_num': 7}}

    # breakpoint()
    process_sdt_pdfs()

    # save_json_log()


def run_script(window):
    global MASTER_DICT, MASTER_LIST

    start_time = datetime.now()
    print('\nLoading Excel File...')
    initialize_master_dicts()
    print('Done!')

    print('\nSearching PDFs...')
    search_and_save_locations()
    print('Done!')

    # for job in JOB_LIST:
    #     print('\nCreating New PDFs...')
    #     merge_pdfs()
    #     print('Done!')
    #
    #     print('\nOpening Output Folder...')
    #     util.open_folder_explorer(OUTPUT.get_field_path())
    #     print('Done!')

        # print('\nClosing Program...')
        # window.close()
        #
        # end_time = datetime.now()
        # run_time = end_time - start_time
        # print('\nProgram Run Time:', run_time)

