from functions.run_python_file import run_python_file

print(run_python_file("calculator", "main.py")) # Should print the calculator's usage instructions

print(run_python_file("calculator", "main.py", ["3 + 5"])) # Should run the calculator... which gives a kinda nasty rendered result

print(run_python_file("calculator", "tests.py")) # Should run the calculator's tests successfully

print(run_python_file("calculator", "../main.py")) # This should return an error

print(run_python_file("calculator", "nonexistent.py")) # This should return an error

print(run_python_file("calculator", "lorem.txt")) # This should return an error
