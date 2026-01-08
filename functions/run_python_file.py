import os
import subprocess

from google.genai import types

# Executes a local Python script in a subprocess and captures the stdout/stderr.
def run_python_file(working_directory, file_path, args=None) -> str:
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_target_file = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory
        
        if valid_target_file is False:
            raise ValueError(f'Cannot execute "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(target_file_path):
            raise ValueError(f'"{file_path}" does not exist or is not a regular file')
        
        if not target_file_path.endswith('.py'):
            raise ValueError(f'"{file_path}" is not a Python file')
           
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, capture_output=True, text=True, cwd=abs_working_directory, timeout=30)

        output_str = ""

        if result.returncode != 0:
            output_str += f"process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output_str += "No output produced\n"
        if result.stdout:
            output_str += f"STDOUT: {result.stdout}\n"
        if result.stderr:
            output_str += f"STDERR: {result.stderr}\n"

        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"

# Defines the API schema for the python execution tool (includes file path and CLI arguments).
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Possible additional arguments to pass to the Python script",
            ),
        },
    ),
)
