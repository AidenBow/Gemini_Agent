import os
from google.genai import types

def write_file(working_directory, file_path, content):

    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_abs_path = os.path.abspath(working_directory)

    if working_directory_abs_path not in file_abs_path :
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    #if not os.path.exists(file_abs_path):
    else:
        with open(file_abs_path, "w") as f:
            f.write(content)
    
    with open(file_abs_path, "r") as f:
        actual_file_content = f.read()
    
    if content == actual_file_content:
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes files or overwrites the file if it already exsits, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we want to write or overwrite, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents we want the file to have",
            )
        },
    ),
)