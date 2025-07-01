import os
from google.genai import types

def get_files_info(working_directory, directory=None):

    directory_abs_path = os.path.abspath(os.path.join(working_directory, directory))
    working_directory_abs_path = os.path.abspath(working_directory)

    if working_directory_abs_path not in directory_abs_path :
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    elif os.path.isfile(directory_abs_path):
        return f'Error: "{directory}" is not a directory'

    else:
        print(f"listing {directory_abs_path} ...")
        for item in os.listdir(directory_abs_path):
            print(f"- {item}: file_size={os.path.getsize(os.path.join(directory_abs_path, item))} bytes, is_dir={os.path.isdir(os.path.join(directory_abs_path, item))}")

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)