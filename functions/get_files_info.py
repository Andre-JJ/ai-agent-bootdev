import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_absolute = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_absolute, directory))

    valid_target_dir = os.path.commonpath([working_dir_absolute, target_dir]) == working_dir_absolute

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    dir_items = os.listdir(target_dir)

    path_info = ""

    for item in dir_items:
        item_size = os.path.getsize(os.path.join(target_dir, item))
        item_dir = os.path.isdir(os.path.join(target_dir, item))

        path_info += f"- {item}: file_size={item_size} bytes, is_dir={item_dir}\n"

    return path_info