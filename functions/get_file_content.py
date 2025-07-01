import os
from google.genai import types

def get_file_content(working_directory, file_path):

    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_abs_path = os.path.abspath(working_directory)
    print(file_abs_path, working_directory_abs_path)

    if working_directory_abs_path not in file_abs_path :
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    elif not os.path.isfile(file_abs_path):
        #print(os.path.isfile(file_abs_path))
        return f'Error: File not found or is not a regular file: "{file_path}"'

    else:
        with open(file_abs_path, "r") as f:
            file_content = f.read(10000)
            if len(file_content) >= 10000:
                file_content = file_content[:10000] + '[...File "{file_path}" truncated at 10000 characters]'
        return file_content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Displays the specified file's content to a max of 10,000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we want to display, relative to the working directory.",
            ),
        },
    ),
)