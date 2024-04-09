import configparser
import sys

import util
import logging
import os
import PySimpleGUI as Gui

CONFIG_FOLDER_PATH: str = "Config Files"
LOG_FILE_PATH: str = os.path.join(CONFIG_FOLDER_PATH, r"Scandoc_Imaging_PDF_Merger_log_file.log")
GUI_CONFIG_PATH: str = os.path.join(CONFIG_FOLDER_PATH, r"gui_config.ini")
OUTPUT_FOLDER_PATH: str = ""


class Gui:
    pass


def launch_gui():
    """
    This function launches gui which prompts user to select where the employee
    excel timesheets, signed blank pdfs, and output folders are located. The user can then
    run the program with the chosen folders.
    :return:
    """
    global SIGNED_BLANK_PDFS_FOLDER_PATH, OUTPUT_FOLDER_PATH, EMPLOYEE_EXCEL_TIMESHEETS_FOLDER
    # load and set gui config settings
    gui_config: configparser.ConfigParser = util.load_gui_settings(GUI_CONFIG_PATH)
    window_title: str = gui_config.get('GUI', 'window_title', fallback='')
    font_family: str = gui_config.get('GUI', 'font_family', fallback='')
    font_size: int = int(gui_config.get('GUI', 'font_size', fallback=0))
    theme: str = gui_config.get('GUI', 'theme', fallback='')
    Gui.set_options(font=(font_family, font_size))
    Gui.theme(theme)

    # Retrieve the previously selected folders
    EMPLOYEE_EXCEL_TIMESHEETS_FOLDER = gui_config.get('Folders', 'Employee_Excel_Timesheets_Folder', fallback='')
    SIGNED_BLANK_PDFS_FOLDER_PATH = gui_config.get('Folders', 'Signed_Employee_Blank_PDFs_Folder', fallback='')
    OUTPUT_FOLDER_PATH = gui_config.get('Folders', 'Output_Folder', fallback='')

    layout: list = util.generate_window_layout(EMPLOYEE_EXCEL_TIMESHEETS_FOLDER,
                                               SIGNED_BLANK_PDFS_FOLDER_PATH, OUTPUT_FOLDER_PATH)

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
            if values[select_list[0]] == '':
                Gui.popup_error("Please Select a Valid Folder First.")
            else:
                util.open_folder_explorer(values[select_list[0]])
        if event == "Automate Employee Timesheets":
            if util.is_valid_path(values["Employee_Excel_Timesheets_Folder"]) and \
                    util.is_valid_path(values["Signed_Employee_Blank_PDFs_Folder"]) and \
                    util.is_valid_path(values["Output_Folder"]):
                pass
                # set_paths_and_save_config_settings(values, gui_config)
                # run_script()
    window.close()

    # WINDOW.close()


def main():
    util.create_program_folders([CONFIG_FOLDER_PATH])
    util.setup_logging(LOG_FILE_PATH)
    try:
        # TODO: LOOK INTO CREATING A DROPDOWN MENU
        launch_gui()
    except Exception as e:
        logging.exception('An error occurred: Please check log file in "Config Files"')