import os
from config import *

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Reads content from a specified file relative to working directory, function returns string, with file contents in plain text. If file is larger than {MAX_CHARS} characters, the file will be trunctated to lenght of {MAX_CHARS} characters.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file from whom we read file content, relative to the working directory",
                },
            },
            "required": ["file_path"],
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
