import os
import eel
from filedialogs import open_file_dialog, open_folder_dialog


def current_user():
    user = os.environ.get("USERNAME").replace(".", " ").title()
    return user


@eel.expose
def choose_file():
    try:
        dialog = open_file_dialog(title="Select File", multiselect=False)
        if dialog:
            if not isinstance(dialog, (list, tuple)):
                dialog = [dialog]
        return dialog

    except IOError as e:
        print(e)


@eel.expose
def choose_files():
    try:
        dialog = open_file_dialog(title="Select File", multiselect=True)

        if not isinstance(dialog, (list, tuple)):
            dialog = [dialog]

        return dialog

    except IOError as e:
        print(e)


@eel.expose
def choose_folder():
    dialog = open_folder_dialog(title="Select Folder")

    if not isinstance(dialog, (list, tuple)):
        dialog = [dialog]

    return dialog
