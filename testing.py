import configparser

import PySimpleGUI as Gui

import util


def foo2():
    # Define the layout for the window with dropdown menu and folder browse boxes
    layout_source = [
        [Gui.Text("Source folder path:"), Gui.Input(key='-SOURCE_FOLDER_PATH-'), Gui.FolderBrowse(key='-BROWSE_SOURCE-')],
        [Gui.Button('OK')]
    ]

    layout_destination = [
        [Gui.Text("Destination folder path:"), Gui.Input(key='-DEST_FOLDER_PATH-'), Gui.FolderBrowse(key='-BROWSE_DEST-')],
        [Gui.Button('OK')]
    ]

    # Initial layout with dropdown menu
    layout = [
        [Gui.Text("Select a folder type:")],
        [Gui.DropDown(values=['Source', 'Destination'], key='-FOLDER_TYPE-', enable_events=False)],
        [Gui.Button('OK')]
    ]

    # Create the window
    window = Gui.Window('Folder Browse Example', layout)

    # Event loop
    while True:
        event, values = window.read()

        if event == Gui.WINDOW_CLOSED:
            break


        # print(f"\n\nvalues = {values}\nevent = {event}")
        # if event == 'OK':
        #     if values['-FOLDER_TYPE-'] == '':
        #         print(f"\n\nvalues = {values}\nevent = {event}")
        #         Gui.popup_error("Please Select a Valid Folder First.")
        #     else:
        #         print(f"\n\nvalues = {type(values)}\nevent = {event}")
        #
        #         if '-FOLDER_TYPE-' in values.keys():
        #             folder_type = values.get('-FOLDER_TYPE-', '')
        #             # breakpoint()
        #             window.close()  # Close the current window
        #         else:
        #             break
        #
        #         # Create a new window with updated layout based on the selected folder type
        #         if folder_type == 'Source':
        #             new_layout = layout_source# + [[sg.Button('OK')]]
        #         else:
        #             new_layout = layout_destination# + [[sg.Button('OK')]]
        #
        #         # breakpoint()
        #
        #         window = Gui.Window('Folder Browse Example', new_layout)



        print(f"\n\nvalues = {values}\nevent = {event}")
        if event == 'OK' and values['-FOLDER_TYPE-'] == '':
            print(f"\n\nvalues = {values}\nevent = {event}")
            Gui.popup_error("Please Select a Valid Folder First.")
        else:
            print(f"\n\nvalues = {type(values)}\nevent = {event}")

            if '-FOLDER_TYPE-' in values.keys():
                folder_type = values.get('-FOLDER_TYPE-', '')
                # breakpoint()
                window.close()  # Close the current window
            else:
                break

            # Create a new window with updated layout based on the selected folder type
            if folder_type == 'Source':
                new_layout = layout_source# + [[sg.Button('OK')]]
            else:
                new_layout = layout_destination# + [[sg.Button('OK')]]

            # breakpoint()

            window = Gui.Window('Folder Browse Example', new_layout)



    # Close the window
    window.close()


def foo1():
    # Define the layout for the window with dropdown menu and text box
    layout = [
        [Gui.Text("Select a folder type:")],
        [Gui.DropDown(values=['Source', 'Destination'], key='-FOLDER_TYPE-', enable_events=True)],
        [Gui.Text("Selected folder type:"), Gui.Input(key='-SELECTED_FOLDER_TYPE-', readonly=True)],
        [Gui.Button('OK')]
    ]

    # Create the window
    window = Gui.Window('Folder Browse Example', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == Gui.WINDOW_CLOSED:
            break

        # Update text box with selected option from dropdown
        if event == '-FOLDER_TYPE-':
            selected_folder_type = values['-FOLDER_TYPE-']
            window['-SELECTED_FOLDER_TYPE-'].update(selected_folder_type)

        # Handle 'OK' button click event
        if event == 'OK':
            selected_folder_type = values['-SELECTED_FOLDER_TYPE-']
            Gui.popup(f"You selected: {selected_folder_type}")
            break

    # Close the window
    window.close()


# def launch_gui_TIMESHEET():
#     """
#     This function launches gui which prompts user to select where the employee
#     excel timesheets, signed blank pdfs, and output folders are located. The user can then
#     run the program with the chosen folders.
#     :return:
#     """
#     global SIGNED_BLANK_PDFS_FOLDER_PATH, OUTPUT_FOLDER_PATH, EMPLOYEE_EXCEL_TIMESHEETS_FOLDER
#     # load and set gui config settings
#     gui_config: configparser.ConfigParser = util.load_gui_settings(GUI_CONFIG_PATH)
#     window_title: str = gui_config.get('GUI', 'window_title', fallback='')
#     font_family: str = gui_config.get('GUI', 'font_family', fallback='')
#     font_size: int = int(gui_config.get('GUI', 'font_size', fallback=0))
#     theme: str = gui_config.get('GUI', 'theme', fallback='')
#     Gui.set_options(font=(font_family, font_size))
#     Gui.theme(theme)
#
#     # Retrieve the previously selected folders
#     EMPLOYEE_EXCEL_TIMESHEETS_FOLDER = gui_config.get('Folders', 'Employee_Excel_Timesheets_Folder', fallback='')
#     SIGNED_BLANK_PDFS_FOLDER_PATH = gui_config.get('Folders', 'Signed_Employee_Blank_PDFs_Folder', fallback='')
#     OUTPUT_FOLDER_PATH = gui_config.get('Folders', 'Output_Folder', fallback='')
#
#     layout: list = util.generate_window_layout(SI_LOGO_PATH, EMPLOYEE_EXCEL_TIMESHEETS_FOLDER,
#                                                SIGNED_BLANK_PDFS_FOLDER_PATH, OUTPUT_FOLDER_PATH)
#
#     window: Gui.PySimpleGUI.Window = Gui.Window(window_title, layout)
#     while True:
#         event: str
#         values: dict
#         event, values = window.read()
#
#         select_list = []
#         try:
#             select_list = event.split(' ')
#         except AttributeError as e:
#             if str(e) == "'NoneType' object has no attribute 'split'":
#                 sys.exit()
#
#         if event in (Gui.WINDOW_CLOSED, "Exit"):
#             break
#         if 'folder' in select_list and 'open' in select_list:
#             if values[select_list[0]] == '':
#                 Gui.popup_error("Please Select a Valid Folder First.")
#             else:
#                 util.open_folder_explorer(values[select_list[0]])
#         if event == "Automate Employee Timesheets":
#             if util.is_valid_path(values["Employee_Excel_Timesheets_Folder"]) and \
#                     util.is_valid_path(values["Signed_Employee_Blank_PDFs_Folder"]) and \
#                     util.is_valid_path(values["Output_Folder"]):
#                 pass
#                 set_paths_and_save_config_settings(values, gui_config)
#                 # run_script()
#     window.close()