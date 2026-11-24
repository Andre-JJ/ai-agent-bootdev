import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "strict": True,
        "description": (
            "Executes an EXISTING Python (.py) file that is already on disk and returns its "
            "exit code (only if non-zero), stdout and stderr. "
            "Takes ONLY 'file_path' and 'args'. It does NOT accept file content or code. "
            "To create or modify a script, call write_file first, then call run_python_file "
            "with just the path."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the .py file to execute, relative to the working directory (e.g. 'main.py').",
                },
                "args": {
                    "type": ["array", "null"],
                    "items": {"type": "string"},
                    "description": (
                        "List of command-line arguments, each as a string (e.g. [\"3 + 7 * 2\"]). "
                        "Pass null if the script needs no arguments."
                    ),
                },
            },
            "required": ["file_path", "args"],
            "additionalProperties": False,
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