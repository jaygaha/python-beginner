# Context manager
# Context managers allow you to allocate and release resources precisely when you want to.
# The most widely used example of context managers is the with statement.
# Suppose you have two related operations which you’d like to execute as a pair, with a block of code in between.
# Context managers allow you to do specifically that.
# The with statement simplifies exception handling by encapsulating standard uses of try/finally statements in so-called context managers.

# Example 1: File handling
def write_file():
    my_file = open('workspace/5_package_managers/test.txt', 'w')
    my_file.write('Hello, Python!')
    my_file.close()

write_file()

# The above code is not efficient because if an exception occurs between the open and close statements, the file will not be closed.
# To ensure that the file is closed, you can use the with statement.

# Example 2: Using with statement
def write_file_with():
    with open('workspace/5_package_managers/test.txt', 'w') as my_file:
        my_file.write('Hello, Python!')

write_file_with()

# The with statement simplifies exception handling by encapsulating standard uses of try/finally statements in so-called context managers.

# Example 3: try/finally statement
def write_file_try():
    my_file = open('workspace/5_package_managers/test.txt', 'w')
    try:
        my_file.write('Hello, Python!')
    except Exception as e:
        print(f'writing to file failed: {e}')
    finally:
        my_file.close()

write_file_try()

# The above code is not efficient because it is more verbose and less readable than the with statement.

# Example 4: Custom context manager

class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
        # The __enter__ method is called at the beginning of the with block.
    def __enter__(self):
        return self.file_obj
    # The __exit__ method is called after the with block finishes execution.
    def __exit__(self, type, value, traceback):
        self.file_obj.close()


def write_file_custom():
    with File('workspace/5_package_managers/test.txt', 'w') as my_file:
        my_file.write('Hello, Python!')

write_file_custom()

# Exception has been handled
class FileExp(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        print("Exception has been handled")
        self.file_obj.close()
        return True

def write_file_custom_exp():
    with FileExp('workspace/5_package_managers/test.txt', 'w') as opened_file:
        opened_file.undefined_function('Hello, Exception Python!')

write_file_custom_exp()

# Generator
from contextlib import contextmanager

@contextmanager
def open_file(name):
    f = open(name, 'w')
    try:
        yield f
    finally:
        f.close()

def write_file_generator():
    with open_file('workspace/5_package_managers/test.txt') as f:
        f.write('Hello, Generator Python!')

write_file_generator()

