import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a python script in a specified path with optional arguments. Function returns return code if it is non zero, stdout and/or stderr",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to python script which we want to run",
                },
                "args": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional list of strings which will be passed as CLI arguments (default is None)",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_absolute = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_absolute, file_path))
        
    if not os.path.commonpath([working_dir_absolute, target_file]) == working_dir_absolute:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]

    if args is not None:
        command.extend(args)

    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=30.0)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = ""

    if process.returncode != 0:
        output += f"Process exited with code {process.returncode}\n"

    if process.stdout == "" and process.stderr == "":
        output += "No output produced\n"

    output += f"STDOUT: {process.stdout}\n"
    output += f"STDERR: {process.stderr}"

    return output