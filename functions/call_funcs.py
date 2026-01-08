from config import WORKING_DIRECTORY
from google.genai import types
from .get_file_content import get_file_content, schema_get_file_content
from .get_files_info import get_files_info, schema_get_files_info
from .run_python_file import run_python_file, schema_run_python_file
from .write_file import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
)

# Maps the API's function call request to a local tool and executes it.
def call_function(function_call, verbose=False) -> google.genai.types.Content:
    print("------------------------------")
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                ),
            ],
        )
    
    args = dict(function_call.args) if function_call.args else {}

    args["working_directory"] = WORKING_DIRECTORY

    function_result = function_map[function_name](**args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)
