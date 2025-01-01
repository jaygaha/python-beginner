# Python write to files (.txt, .csv, .json)

import csv
import json


text_data = "Hello, World!"

file_path = "workspace/3_oops/output.txt"
xfile_path = "workspace/3_oops/output_x.txt"
employees = ["John", "Doe", "Jane", "Doe"]

# w: write, a: append, r: read, x: create
with open(file_path, "w") as file:
    file.write(text_data)
    print(f"Data written to {file_path}.")

try:
    with open(xfile_path, "x") as file:
        file.write(text_data)
        print(f"Data written to {xfile_path}.")
except FileExistsError:
    print(f"File already exists in {xfile_path}.")

try:
    with open(file_path, "a") as file:
        file.write("\n" +text_data)
        print(f"Data written to {file_path}.")
        for employee in employees:
            file.write("\n" +employee)
except FileExistsError:
    print(f"File already exists in {file_path}.")


#JSON

jfile_path = "workspace/3_oops/output.json"

student = {
    "name": "John Doe",
    "age": 25,
    "grade": "A"
}

try:
    with open(jfile_path, "w") as file:
        json.dump(student, file, indent=4)
        print(f"JSON Data written to {jfile_path}.")
except FileExistsError:
    print(f"File already exists in {jfile_path}.")

# CSV

students = [["Name", "Age", "Grade"],
    ["John Doe", 25, "A"],
    ["Jane Doe", 24, "B"],
    ["Jim Doe", 23, "C"],
    ["Jill Doe", 22, "D"]]

cfile_path = "workspace/3_oops/output.csv"

try:
    with open(cfile_path, "w", newline="") as file:
        writer = csv.writer(file)
        for row in students:
            writer.writerow(row)
        print(f"CSV Data written to {cfile_path}.")

except FileExistsError:
    print(f"File already exists in {cfile_path}.")