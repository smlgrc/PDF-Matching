import configparser
import logging
import os
import subprocess
from logging.handlers import RotatingFileHandler
from pathlib import Path

import PySimpleGUI as Gui


def clear_folder(folder_path: str):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clear_folder(file_path)  # Recursively clear subdirectories
            os.rmdir(file_path)  # Remove the empty directory


def clear_program_folders(path_list: list):
    for path in path_list:
        if os.path.exists(path):
            clear_folder(path)


def create_program_folders(path_list: list):
    for path in path_list:
        if not os.path.exists(path):
            os.makedirs(path)


def setup_logging(log_file):
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=1)
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def open_folder_explorer(path):
    # Check if the path exists
    if os.path.exists(path):
        # Open the file explorer window to the specified path
        subprocess.Popen(f'explorer "{os.path.abspath(path)}"')
    else:
        Gui.popup_error("Missing or Invalid Filepath(s)\nPlease check that you've selected all folders")


def is_valid_path(filepath: str):
    if filepath and Path(filepath).exists():
        return True
    Gui.popup_error("Missing or Invalid Filepath(s)\nPlease check that you've selected all folders")
    return False


def load_gui_settings(gui_path: str) -> configparser.ConfigParser:
    # Check if config.ini file exists
    if not os.path.isfile(gui_path):
        # Create config.ini file with default settings
        config = configparser.ConfigParser()
        config['GUI'] = {
            'window_title': 'Scandoc Imaging Pdf Merger',
            'font_size': '14',
            'font_family': 'Arial',
            'theme': 'LightBlue3'
        }
        with open(gui_path, 'w') as configfile:
            config.write(configfile)
    # return config file
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(gui_path)
    return config


def generate_window_layout(employee_excel_timesheets_folder, signed_blank_pdfs_folder_path, output_folder_path) -> list:
    return [
        [
            Gui.Column([
            ], element_justification='center', justification='center'),
        ],
        [
            Gui.Column([
                [
                    Gui.Text(text='\nTimesheet Automation Program\n', font=('Ariel', 25)),
                ],
            ], element_justification='center', justification='center'),
        ],
        [
            Gui.Column([
                [
                    Gui.Text("Employee Excel Timesheets Folder:"),
                    Gui.Input(key="Employee_Excel_Timesheets_Folder", default_text=employee_excel_timesheets_folder, size=(60, 0)),
                    Gui.FolderBrowse(button_text="Select Folder"),
                    Gui.Button(button_text="Open Folder", key="Employee_Excel_Timesheets_Folder folder open")
                ],
                [
                    Gui.Text("Signed Employee Blank PDFs Folder:"),
                    Gui.Input(key="Signed_Employee_Blank_PDFs_Folder", default_text=signed_blank_pdfs_folder_path, size=(60, 0)),
                    Gui.FolderBrowse(button_text="Select Folder"),
                    Gui.Button(button_text="Open Folder", key="Signed_Employee_Blank_PDFs_Folder folder open")
                ],
                [
                    Gui.Text("Output Folder:"),
                    Gui.Input(key="Output_Folder", default_text=output_folder_path, size=(60, 0)),
                    Gui.FolderBrowse(button_text="Select Folder"),
                    Gui.Button(button_text="Open Folder", key="Output_Folder folder open")
                ],
            ], element_justification='right', pad=(0, 40))
        ],
        [
            Gui.Column([
                [
                    Gui.Exit(s=16, button_color="tomato"), Gui.Button("Automate Employee Timesheets")
                ]
            ], justification='center')
        ]
    ]