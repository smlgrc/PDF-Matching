import configparser
import sys

import generate_defense_and_insurance_pdfs
import generate_invoice_pdfs
import testing
import util
import logging
import os
import PySimpleGUI as Gui


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
GUI_CONFIG_PATH: str = os.path.join(CONFIG_FOLDER_PATH, r"gui_config.ini")

PROGRAM_FILES_PATH: str = resource_path("Program Files")
SI_LOGO_PATH: str = resource_path(os.path.join(PROGRAM_FILES_PATH, r"si_logo_path.png"))


def set_paths_and_save_config_settings(values: dict, config: configparser.ConfigParser):
    """
    This function sets paths from values dictionary to global variables and saves them to
    the gui_config.ini file so that when the user runs the program again, the previously
    chosen paths will populate the input boxes.
    :param values: file paths of previously user chosen folders
    :param config: config object used to update and save file paths to config ini file
    """
    global SIGNED_BLANK_PDFS_FOLDER_PATH, OUTPUT_FOLDER_PATH, EMPLOYEE_EXCEL_TIMESHEETS_FOLDER

    # Create the 'Folders' section if it doesn't exist
    if 'Folders' not in config:
        config['Folders'] = {}

    # set global values and gui config variables to whatever is in the window
    EMPLOYEE_EXCEL_TIMESHEETS_FOLDER = config['Folders']['Employee_Excel_Timesheets_Folder'] = values["Employee_Excel_Timesheets_Folder"]
    SIGNED_BLANK_PDFS_FOLDER_PATH = config['Folders']['Signed_Employee_Blank_PDFs_Folder'] = values["Signed_Employee_Blank_PDFs_Folder"]
    OUTPUT_FOLDER_PATH = config['Folders']['Output_Folder'] = values["Output_Folder"]

    with open(GUI_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)


def launch_gui():
    try:
        # Initial layout with dropdown menu
        layout = [
            [Gui.Text("Select a folder type:")],
            [Gui.DropDown(values=['Invoices', 'Defense & Insurance'], key='-FOLDER_TYPE-', enable_events=False)],
            [Gui.Exit(s=16, button_color="tomato"), Gui.Button('OK')]
        ]

        # Create the window
        window = Gui.Window('Folder Browse Example', layout)

        # Event loop
        while True:
            folder_type: str = ''
            event, values = window.read()

            # Handle event when dropdown menu value changes
            if event in (Gui.WINDOW_CLOSED, "Exit"):
                break
            if event == 'OK' and values['-FOLDER_TYPE-'] == '':
                # print(f"\n\ntype(values) = {type(values)}\nvalues = {values}\nevent = {event}")
                Gui.popup_error("Please Select a Valid Folder First.")
            else:
                # print(f"\n\ntype(values) = {type(values)}\nvalues = {values}\nevent = {event}")
                if '-FOLDER_TYPE-' in values.keys():
                    folder_type = values.get('-FOLDER_TYPE-', '')
                    window.close()  # Close the current window

                # Create a new window with updated layout based on the selected folder type
                if folder_type == 'Invoices':
                    generate_invoice_pdfs.launch_gui()
                elif folder_type == 'Defense & Insurance':
                    generate_defense_and_insurance_pdfs.launch_gui()

        # Close the window
        # window.close()
    except Exception as e:
        Gui.popup_error(f"An error occurred: Please check log file in 'Config Files'\n\nError: {e}\n")
        logging.exception(f'An error occurred: Please check log file in "Config Files"')


def main():
    util.create_program_folders([CONFIG_FOLDER_PATH])
    util.setup_logging(LOG_FILE_PATH)
    launch_gui()


if __name__ == '__main__':
    main()
