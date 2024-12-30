from dunder_name1 import *


# print(__name__)

def favorite_drink(drink):
    print(f"Your favorite drink is {drink}")

def main():
    print("This is dunders 2")
    favorite_food("Sushi")
    favorite_drink("Barley tea")
    print("Have a nice lunch!")

if __name__ == "__main__":
    main()