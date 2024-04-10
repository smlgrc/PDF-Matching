import PySimpleGUI as sg


def foo2():
    # Define the layout for the window with dropdown menu and folder browse boxes
    layout_source = [
        [sg.Text("Source folder path:"), sg.Input(key='-SOURCE_FOLDER_PATH-'), sg.FolderBrowse(key='-BROWSE_SOURCE-')],
        [sg.Button('OK')]
    ]

    layout_destination = [
        [sg.Text("Destination folder path:"), sg.Input(key='-DEST_FOLDER_PATH-'), sg.FolderBrowse(key='-BROWSE_DEST-')],
        [sg.Button('OK')]
    ]

    # Initial layout with dropdown menu
    layout = [
        [sg.Text("Select a folder type:")],
        [sg.DropDown(values=['Source', 'Destination'], key='-FOLDER_TYPE-', enable_events=True)],
        [sg.Button('OK')]
    ]

    # Create the window
    window = sg.Window('Folder Browse Example', layout)

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # Handle event when dropdown menu value changes
        if event == 'OK':
            print(f"\n\nvalues = {values}\nevent = {event}")

            if '-FOLDER_TYPE-' in values:
                folder_type = values['-FOLDER_TYPE-']
                window.close()  # Close the current window
            else:
                break

            # Create a new window with updated layout based on the selected folder type
            if folder_type == 'Source':
                new_layout = layout_source# + [[sg.Button('OK')]]
            else:
                new_layout = layout_destination# + [[sg.Button('OK')]]

            # breakpoint()

            window = sg.Window('Folder Browse Example', new_layout)

    # Close the window
    window.close()


def foo1():
    # Define the layout for the window with dropdown menu and text box
    layout = [
        [sg.Text("Select a folder type:")],
        [sg.DropDown(values=['Source', 'Destination'], key='-FOLDER_TYPE-', enable_events=True)],
        [sg.Text("Selected folder type:"), sg.Input(key='-SELECTED_FOLDER_TYPE-', readonly=True)],
        [sg.Button('OK')]
    ]

    # Create the window
    window = sg.Window('Folder Browse Example', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        # Update text box with selected option from dropdown
        if event == '-FOLDER_TYPE-':
            selected_folder_type = values['-FOLDER_TYPE-']
            window['-SELECTED_FOLDER_TYPE-'].update(selected_folder_type)

        # Handle 'OK' button click event
        if event == 'OK':
            selected_folder_type = values['-SELECTED_FOLDER_TYPE-']
            sg.popup(f"You selected: {selected_folder_type}")
            break

    # Close the window
    window.close()

