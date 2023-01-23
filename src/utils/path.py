from os.path import dirname, abspath
import os
import importlib


def _is_module(filename):
    return filename.endswith(".py") and not filename.startswith("__")


def _get_current_path(absolute_file):
    root_path = os.getcwd()
    folder = (
        abspath(dirname(absolute_file))
        .replace(root_path, "")
        .lstrip("\\")
        .replace("\\", "/")
    )

    return folder


def get_modules(absolute_file: str, name: str):
    current_folder = _get_current_path(absolute_file)

    modules = []

    for filename in os.listdir(current_folder):
        if _is_module(filename):
            module_name = filename[:-3]
            module = importlib.import_module(
                name=f".{module_name}", package=current_folder.replace("/", ".")
            )
            modules.append(getattr(module, name))

    return modules
