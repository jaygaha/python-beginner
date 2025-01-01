# Python file detection

import os

# file_path = "workspace/3_oops/test.txt"
file_path = "workspace/3_oops"

if os.path.exists(file_path):
    print(f"File exists in {file_path}.")

    if os.path.isfile(file_path):
        print(f"File is a regular file.")
    elif os.path.isdir(file_path):
        print(f"File is a directory.")
else:
    print(f"File does not exist in {file_path}.")