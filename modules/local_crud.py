import json


def read_save_file(path=None):
    if path is None:
        path = "save.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    return data


def restore_default_save_file():
    default_data = read_save_file("default_save.json")

    return default_data


def write_save_file(data, path=None):
    if path is None:
        path = "save.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
