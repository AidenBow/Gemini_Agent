import os, subprocess, sys
from google.genai import types

def run_python_file(working_directory, file_path):

    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_abs_path = os.path.abspath(working_directory)

    if working_directory_abs_path not in file_abs_path :
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    elif not os.path.exists(file_abs_path):
        #print(os.path.isfile(file_abs_path))
        return f'Error: File "{file_path}" not found.'

    elif file_abs_path[-3:] != ".py":
        print(file_abs_path[-3:])
        return f'Error: "{file_path}" is not a Python file.'
    
    else:
        try:
            print(f"trying {file_abs_path}")
            output = subprocess.run([sys.executable, file_abs_path], capture_output=True, timeout=10, check=True)
            formatted_output = f'STDOUT: {output.stdout} \nSTDERR: {output.stderr}'
            if output.returncode != 0:
                formatted_output += f'\n Process exited with code {output.returncode}'
            
            if formatted_output == "":
                formatted_output = "No output produced."
            
            return formatted_output

        except subprocess.CalledProcessError as e:
            return f'Error: executing Python file: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we want to run, relative to the working directory.",
            ),
        },
    ),
)