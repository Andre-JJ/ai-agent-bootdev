import os
from config import *

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_absolute = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_absolute, file_path))

    if not os.path.commonpath([working_dir_absolute, target_file]) == working_dir_absolute:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        file = open(target_file, "r")
    except OSError as e:
        return f"Error: Opening the file threw exception: {e}" 

    with file as f:
        file_content = f.read(MAX_CHARS)

        if f.read(1):
            file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    return file_content
