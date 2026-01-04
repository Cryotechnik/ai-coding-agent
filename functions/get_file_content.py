import os

from config import MAX_CHARS_LIMIT

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
        
        if valid_target_file is False:
            raise ValueError(f"Cannot read '{file_path}' as it is outside the permitted working directory")

        if not os.path.isfile(target_file):
            raise ValueError(f"File not found or is not a regular file: '{file_path}'")
        
        with open(target_file, 'r') as f:
            file_content_str = f.read(MAX_CHARS_LIMIT)
            if f.read(1):
                file_content_str += f"[...File '{file_path}' truncated at {MAX_CHARS_LIMIT} characters]"
        
        return file_content_str
    
    except Exception as e:
        return f"Error: {e}"