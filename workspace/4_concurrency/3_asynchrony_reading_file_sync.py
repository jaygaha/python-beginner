# Reading Files (Concurrent I/O tasks)
# Synchronous Reading Files

import time

def read_file_sync(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_all_sync(file_paths):
    return [read_file_sync(file_path) for file_path in file_paths]

file_paths = [
    'workspace/4_concurrency/output1.txt',
    'workspace/4_concurrency/output2.txt',
    'workspace/4_concurrency/output3.txt']

# start time
start_time = time.perf_counter()

data = read_all_sync(file_paths)

# end time
end_time = time.perf_counter() - start_time

print(data)
print()
print(f"executed in {end_time:0.2f} seconds.")
