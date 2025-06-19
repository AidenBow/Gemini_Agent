import os

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
    