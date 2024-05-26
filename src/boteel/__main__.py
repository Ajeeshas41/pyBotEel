import sys
import os

sys.path.append(os.path.curdir)

from typing import List
from boteel.core.utils.filehandler import copy_files
import boteel


def update_settings(func):
    def decorator(*args, **kwargs):
        settings_changed: bool = False
        if boteel.settings.debug:
            print("modifying settings.py file")
            lines = ""
            debug_line = ""
            with open(
                os.path.join(boteel.BASE_DIR, "settings.py"), "r", encoding="UTF-8"
            ) as file:
                lines = file.readlines()

            for idx, line in enumerate(lines):
                if line.startswith("DEBUG"):
                    debug_line = "DEBUG = False\n"
                    lines[idx] = debug_line
                    break

            with open(
                os.path.join(boteel.BASE_DIR, "settings.py"), "w", encoding="UTF-8"
            ) as file:
                file.writelines(lines)
                settings_changed = True
        # ==============================
        response = func(*args, **kwargs)
        # ==============================
        if settings_changed:
            print("reverting settings.py file")
            for idx, line in enumerate(lines):
                if line.startswith("DEBUG"):
                    debug_line = "DEBUG = True\n"
                    lines[idx] = debug_line
                    break

            with open(
                os.path.join(boteel.BASE_DIR, "settings.py"), "w", encoding="UTF-8"
            ) as file:
                file.writelines(lines)

        return response

    return decorator


@update_settings
def _corepackager(main_script: str, web_folder: str, unknown_args: List[str] = None):
    import pkg_resources as pkg
    import PyInstaller.__main__ as pyi

    if not unknown_args:
        unknown_args = []

    print(
        "Building executable with main script '%s' and web folder '%s'...\n"
        % (main_script, web_folder)
    )

    eel_js_file: str = pkg.resource_filename("eel", "eel.js")
    js_file_arg: str = "%s%seel" % (eel_js_file, os.pathsep)
    web_folder_arg: str = "%s%s%s" % (web_folder, os.pathsep, web_folder)

    needed_args: List[str] = [
        "--hidden-import",
        "bottle_websocket",
        "--hidden-import",
        "pyodbc",
        "--add-data",
        "settings.py;.",
        "--add-data",
        js_file_arg,
        "--add-data",
        web_folder_arg,
        "--noconfirm",
    ]

    for app in boteel.settings.installed_apps:
        needed_args.extend(
            ["--hidden-import", app, "--hidden-import", "%s.urls" % app]
        )
    
    for middleware in boteel.settings.middlewares:
        needed_args.extend(
            ["--hidden-import", middleware.rsplit(".", 1)[0]]
        )

    for context in boteel.settings.context_data:
        needed_args.extend(
            ["--hidden-import", context.rsplit(".", 1)[0]]
        )

    name_arg = ["--name", boteel.settings.app_title]

    full_args: List[str] = [main_script] + name_arg + needed_args + unknown_args

    print("Running:\npyinstaller", " ".join(full_args), "\n")

    pyi.run(full_args)


def packager():
    from boteel.core.boteel import source_settings
    source_settings()

    # Collect static files into single directory
    print("copying the static files")
    # copy_folders = ["static", "templates"]
    # for folder in copy_folders:
    #     for app, _dir in backend.app_dict.items():
    #         src = os.path.join(os.path.abspath(_dir), folder, app)
    #         dst = os.path.join(backend.BASE_DIR, "static", folder, app)
    #         copy_files(src=src, dst=dst)

    main_script = "main.py"
    web_folder = "static"
    _corepackager(main_script=main_script, web_folder=web_folder)

def collectstatic():
    from boteel.core.boteel import source_settings
    settings = source_settings()
    print("copying the static files")
    
    copy_folders = ["static", "templates"]
    for app, folder in boteel.app_dict.items():
        for end_dir in copy_folders:
            src = os.path.join(settings.BASE_DIR, folder, end_dir, app)
            dst = os.path.join(settings.BASE_DIR, "static", end_dir, app)
            copy_files(src=src, dst=dst)

args = sys.argv
if "--create" in args:
    print("Create template called")
elif "--collectstatic" in args:
    collectstatic()
else:
    print("Packager called")
    # packager()