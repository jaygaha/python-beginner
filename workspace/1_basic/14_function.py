# function: A block of reusable code; place () after the name to invoke it

def happy_birthday():
    print("Happy birthday to you!")
    print("You are old!")
    print("Happy birthday to you!")
    print()


happy_birthday()
happy_birthday()

def greet(name):
    print("Welcome!")
    print(f"Good morning, {name}")
    print()

greet("Laure")


def display_invoice(username, amount, due_date):
    print(f"Hello, {username}")
    print(f"Your bill of ${amount} is due: {due_date}")
    print()


display_invoice("John doe", 99.99, "Jan 25")