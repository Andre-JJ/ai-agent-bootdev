import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "strict": True,
        "description": (
            "Creates or completely overwrites a file with the given text. Parent directories are "
            "created if missing. This only writes; it does NOT run anything. To execute a Python "
            "file afterwards, call run_python_file with the path. Always pass the FULL new file "
            "contents, not a diff or snippet."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to write, relative to the working directory (e.g. 'calculator/pkg/calculator.py').",
                },
                "content": {
                    "type": "string",
                    "description": "The complete text the file should contain after writing.",
                },
            },
            "required": ["file_path", "content"],
            "additionalProperties": False,
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_absolute = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_absolute, file_path))
    
    if not os.path.commonpath([working_dir_absolute, target_file]) == working_dir_absolute:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    if os.path.dirname(target_file) != "":
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

    try:
        file = open(target_file, "w")
    except OSError as e:
        return f"Error: Opening the file threw exception: {e}"

    with file as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'