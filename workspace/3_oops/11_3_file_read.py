# Python reading files (.txt, .csv, .json)

import csv
import json


file_path = 'workspace/3_oops/output.txt'
nfile_path = 'workspace/3_oops/no-exists.txt'

# r= read, w= write, a= append, r+= read and write
with open(file_path, 'r') as file:
    content = file.read()
    print(content)

try:
    with open(nfile_path, 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print('File not found')

try:
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print('File not found')
except PermissionError:
    print('Permission denied')

# JSON
jfile_path = 'workspace/3_oops/output.json'

try:
    with open(jfile_path, 'r') as file:
        content = json.load(file)
        print(content)
        print(content['name'])
except FileNotFoundError:
    print('File not found')
except PermissionError:
    print('Permission denied')


# CSV
cfile_path = 'workspace/3_oops/output.csv'

try:
    with open(cfile_path, 'r') as file:
        content = csv.reader(file)
        for line in content:
            print(line)
            print(line[0])
            print(line[1])
except FileNotFoundError:
    print('File not found')
except PermissionError:
    print('Permission denied')

