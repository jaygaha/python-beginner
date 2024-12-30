# 21 if __name__ == __main__
# this script can be imported OR run standalone
# Functions and classes in this module can be reused without the main block of code executing

# from dunder_name2 import *

# print(__name__) # __main__

def favorite_food(food):
    print(f"Your favorite food is {food}")

def main():
    print("This is dunders script 1")
    favorite_food("MoMo")
    print("Bye!")

if __name__ == "__main__":
    main()