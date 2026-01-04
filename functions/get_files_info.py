import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_working_directory, directory))
        valid_target_dir = os.path.commonpath([abs_working_directory, target_directory]) == abs_working_directory
        file_info = [f"Results for '{directory}':",]
        
        if valid_target_dir is False:
            raise ValueError(f"Cannot list '{directory}' as it is outside the permitted working directory")

        if not os.path.isdir(target_directory):
            raise ValueError(f"'{directory}' is not a directory")
        
        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            file_info.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(file_info)
    
    except Exception as e:
        return f"Error: {e}"