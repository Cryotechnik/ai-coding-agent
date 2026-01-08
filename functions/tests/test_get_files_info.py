from functions.get_files_info import get_files_info

print(get_files_info("calculator", ".")) # Should list all files and directories in the calculator directory

print(get_files_info("calculator", "pkg")) # Should list all files and directories in the pkg subdirectory

print(get_files_info("calculator", "/bin")) # This should return an error

print(get_files_info("calculator", "../")) # This should return an error
