# Iterators and Generators

# Iterators: __iter__() and __next__() methods
# an iterator is an object that contains a countable number of values such as a list, tuple, or string

# Generator: a function that returns an iterator

#  Quiz: Implement my_enumerate

lessons = ["Why Python Programming", "Data Types and Operators", "Control Flow", "Functions", "Scripting"]

def my_enumerate(iterable, start=0):
    # Implement your generator function here
    count = start
    for item in iterable:
        # print(  count, item)
        yield count, item
        count += 1

    # return count

for i, lesson in my_enumerate(lessons, 1):
    print("Lesson {}: {}".format(i, lesson))


print()
# Quiz: Chunker

def chunker(iterable, size):
    """
    Yield successive n-sized chunks from iterable. That means that the last chunk will be smaller than n
    if the length of the iterable isn't a multiple of n.
    """
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size] # yielding i to i + size that means that the last chunk will be smaller than n

for chunk in chunker(range(25), 4):
    print(list(chunk))