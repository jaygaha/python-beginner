# Import: Importing a Module or custom Module

import useful_functions as uf

scores = [70, 35, 82, 23, 98]

mean = uf.mean(scores)
curved = uf.add_five(scores)

mean_c = uf.mean(curved)

print("Scores:", scores)
print("Original Mean:", mean, " New Mean:", mean_c)

print(__name__)
print(uf.__name__)

# Standard Library
# Every module in the standard library is lowercased
# https://pymotw.com/3/

import math

# Quiz: Compute an exponential value

print(math.exp(3)) # 20.085536923187664

# Quiz: Password Generator
import random

# We begin with an empty `word_list`
word_file = "workspace/50_udacity/6_scripts/quiz/words.txt"
word_list = []

# We fill up the word_list from the `words.txt` file
with open(word_file, "r") as words:
    for word in words:
        # remove white space and make everything lowercase
        word = word.strip().lower()
        # don't include words that are too long or too short
        if 3 < len(word) < 8:
            word_list.append(word)

# TODO: Add your function generate_password below
# It should return a string consisting of three random words
# concatenated together without spaces
# def generate_password():
#     password = random.choice(word_list) + random.choice(word_list) + random.choice(word_list)
#     return password

# Alternate solution
def generate_password():
    return ''.join(random.sample(word_list,3))

# Now we test the function
print(generate_password())

# Which module can tell you the current time and date?
# https://docs.python.org/3/library/datetime.html

# Which module has a method for changing the current working directory?
# https://docs.python.org/3/library/os.html

# Which module can read data from a comma separated values (.csv) file into Python dictionaries for each row?
# https://docs.python.org/3/library/csv.html

# Which module can help extract all of the files from a zip file?
# https://docs.python.org/3/library/zipfile.html

# Which module can say how long your code took to run?
# https://docs.python.org/3/library/timeit.html
#  timeit(opens in a new tab) for short pieces of code or cProfile or profile(opens in a new tab) for bigger jobs.

# Techniques for Importing Modules

# 1 To import an individual function or class from a module:
# from useful_functions import mean

# 2 To import multiple individual objects from a module:
# from useful_functions import mean, add_five

# 3 To rename a module:
# import useful_functions as uf

# 4 To import an object from a module and rename it:
# from useful_functions import mean as average

# 5 To import every object individually from a module (DO NOT DO THIS):
# from useful_functions import *

# 6 If you really want to use all of the objects from a module, use the standard import module_name statement
# instead and access each of the objects with the dot notation.
# import useful_functions

# Modules, Packages, and Names
# import package_name.submodule_name

# Third Party Modules
# anaconda install -c conda-forge beautifulsoup4
# pip install beautifulsoup4

# requirements.txt: It is a text file that lists all of the Python packages that your project needs to run.
# pip install -r requirements.txt

# Experimenting with an Interpreter
# python3 | python
# ipython: an interactive Python shell