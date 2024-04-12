import configparser
import logging
import os
import subprocess
from logging.handlers import RotatingFileHandler
from pathlib import Path

import PySimpleGUI as Gui


class FileSystemObject:
    def __init__(self, field_name, field_path, field_path_name, field_type):
        self.field_name: str = field_name
        self.field_path: str = field_path
        self.field_path_name: str = field_path_name
        self.field_type: str = field_type

    def set_field_name(self, field_name): self.field_name = field_name
    def set_field_path(self, field_path): self.field_path = field_path
    def set_field_path_name(self, field_path_name): self.field_path_name = field_path_name
    def set_field_type(self, field_type): self.field_type = field_type

    def get_field_name(self): return self.field_name
    def get_field_path(self): return self.field_path
    def get_field_path_name(self): return self.field_path_name
    def get_field_type(self): return self.field_type

    def get_gui_field(self):
        gui_list = [
            Gui.Text(f"{self.field_name}:"),
            Gui.Input(key=f"{self.field_name}", default_text=self.field_path, size=(60, 0))
        ]
        if self.field_type == 'File':
            gui_list.append(Gui.FileBrowse(button_text=f'Select {self.field_type}'))
        else:
            gui_list.append(Gui.FolderBrowse(button_text=f'Select {self.field_type}'))
        gui_list.append(Gui.Button(button_text="Open Folder", key=f"{self.field_name} folder open"))
        return gui_list

    def is_path_valid(self): return verify_path(self.field_path)

    def __str__(self): return self.field_name


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


def verify_path(filepath: str):
    if filepath and Path(filepath).exists():
        return True
    return False


def verify_paths(paths: dict, objects: list[FileSystemObject]):
    for object in objects:
        if not verify_path(paths.get(object.get_field_name(), '')):
            return False
    return True


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


def generate_window_layout(si_logo_path, program_title, project_objects: list[FileSystemObject]) -> list:
    select_paths = []
    for object in project_objects:
        select_paths.append(object.get_gui_field())
    return [
        [
            Gui.Column([
                [
                    Gui.Image(source=si_logo_path),
                ],
            ], element_justification='center', justification='center'),
        ],
        [
            Gui.Column([
                [
                    Gui.Text(text=f'\n{program_title}\n', font=('Ariel', 25)),
                ],
            ], element_justification='center', justification='center'),
        ],
        [
            Gui.Column(select_paths, element_justification='right', pad=(0, 40))
        ],
        [
            Gui.Column([
                [
                    Gui.Exit(s=16, button_color="tomato"), Gui.Button("Generate PDF Files")
                ]
            ], justification='center')
        ]
    ]
