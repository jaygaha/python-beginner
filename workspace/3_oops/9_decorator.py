# Decorator: A function that takes another function as an argument and adds some kind of functionality and returns another function
# without altering the source code of the original function that is passed as an argument.
# Pass the base function as an argument to the decorator function and return the modified function.
#
#   @add_sprinkles
#   get_icecream("Vanilla")

def add_sprinkles(func):
    # wrapper function is needed to avoid calling the function directly
    def wrapper(*args, **kwargs):
        print(f"*Adding sprinkles 🎉*")
        func(*args, **kwargs)
    return wrapper

def add_fudge(func):
    def wrapper(*args, **kwargs):
        print(f"*Adding fudge 🍫*")
        func(*args, **kwargs)
    return wrapper

@add_sprinkles
@add_fudge
def get_icecream(flavor):
    print(f"Here is your {flavor} icecream 🍦")

get_icecream("Vanilla")