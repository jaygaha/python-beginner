# To create a iterator, we need to implement __iter__() and __next__() methods in the class.

# Example: Create an iterator that returns numbers, starting with 1, and each sequence will increase by one (returning 1, 2, 3, 4, 5, ...)
# Stop after 5 iterations
class MyNumbers:
    # __iter__() method acts similar to __init__() method in a class
    def __iter__(self):
        self.a = 1
        return self

    # __next__() method will return the next value
    def __next__(self):
        if self.a <= 5:
            x = self.a
            self.a += 1
            return x
        else:
            # StopIteration is raised to signal that the iteration is done
            raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

# We can also use a for loop to iterate through the iterator
for x in myclass:
    print(x) # 1 2 3 4 5


# print(next(myiter)) # 1
# print(next(myiter)) # 2
# print(next(myiter)) # 3
# print(next(myiter)) # 4
# print(next(myiter)) # 5
# print(next(myiter)) # StopIteration exception