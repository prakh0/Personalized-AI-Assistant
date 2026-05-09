import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getenv("FILE_DIR")


def find_file(file_name: str):
    file_name = file_name.lower()

    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if file_name in f.lower():
                return os.path.join(root, f)
    return None


def get_relative_path(full_path: str):
    return os.path.relpath(full_path, BASE_DIR)


def get_full_path(relative_path: str):
    full_path = os.path.abspath(os.path.join(BASE_DIR, relative_path))
    if not full_path.startswith(BASE_DIR):
        raise ValueError("Invalid path")
    return full_path
