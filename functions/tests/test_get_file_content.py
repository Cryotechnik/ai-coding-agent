from functions.get_file_content import get_file_content

print(get_file_content("calculator", "lorem.txt")) # Should print the contents of the lorem.txt file

print(get_file_content("calculator", "main.py")) # Should print the contents of the main.py file

print(get_file_content("calculator", "pkg/calculator.py")) # Should print the contents of the pkg/calculator.py file

print(get_file_content("calculator", "/bin/cat")) # This should return an error

print(get_file_content("calculator", "pkg/does_not_exist.py")) # This should return an error
