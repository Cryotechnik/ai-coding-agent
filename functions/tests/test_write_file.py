from functions.write_file import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")) # Should overwrite the contents of the lorem.txt file

print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")) # Should create a new file pkg/morelorem.txt with the given content (if it doesn't already exist)

print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed")) # This should return an error
