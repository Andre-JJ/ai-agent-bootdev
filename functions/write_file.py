import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes specified text content to a specified file whose file path is relative to working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file to which we write content to",
                },
                "content": {
                    "type": "string",
                    "description": "Content in form of text which needs to be written into file",
                },
            },
            "required": ["file_path", "content"],
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