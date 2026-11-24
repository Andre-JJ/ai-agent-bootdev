import os
from config import *

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "strict": True,
        "description": (
            "Reads a file and returns its contents as plain text. Use it to inspect code before "
            f"modifying it. Output is truncated to {MAX_CHARS} characters for larger files. "
            "Takes only 'file_path'. It does not run or modify the file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to read, relative to the working directory (e.g. 'main.py').",
                },
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
    },
}

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
