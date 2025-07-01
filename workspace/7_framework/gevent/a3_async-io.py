# File I/O Operations
#

import gevent
import os
import tempfile


def write_file(filename, content):
    """
    Write content to a file asynchronously

    A context switch in gevent is done through yielding. In this example we have two contexts which yield to each other through invoking gevent.sleep(0).

    Note: For true async file I/O, you'd need gevent's file objects
    or use gevent.fileobject.FileObject
    """
    print(f"Writing to {filename}")
    gevent.sleep(0.1)  # Simulate I/O delay

    with open(filename, 'w') as f:
        f.write(content)

    print(f"Finished writing to {filename}")
    return f"Written to {filename}"


def read_file(filename):
    """Read content from a file asynchronously"""
    print(f"Reading from {filename}")
    gevent.sleep(0.1)  # Simulate I/O delay

    try:
        with open(filename, 'r') as f:
            content = f.read()
        print(f"Finished reading from {filename}")
        return content
    except FileNotFoundError:
        return f"File {filename} not found"

# Create temporary directory for demo
temp_dir = tempfile.mkdtemp()
files = [
    (os.path.join(temp_dir, 'file1.txt'), 'Content of file 1'),
    (os.path.join(temp_dir, 'file2.txt'), 'Content of file 2'),
    (os.path.join(temp_dir, 'file3.txt'), 'Content of file 3'),
]

# Write files concurrently
print("*** Writing files concurrently ***")
write_greenlets = [gevent.spawn(write_file, filename, content)
                  for filename, content in files]
gevent.joinall(write_greenlets)

# Read files concurrently
print("\n*** Reading files concurrently ***")
read_greenlets = [gevent.spawn(read_file, filename)
                 for filename, _ in files]
gevent.joinall(read_greenlets)

# Print results
for greenlet in read_greenlets:
    print(f"Read result: {greenlet.value}")

# Cleanup
import shutil
shutil.rmtree(temp_dir)
