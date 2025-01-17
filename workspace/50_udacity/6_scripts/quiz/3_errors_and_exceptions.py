# Errors and Exceptions
# 1 SyntaxError

# SyntaxError is a built-in exception that is raised when there is an error in the syntax of the program.
# SyntaxError is a subclass of Exception.

# SyntaxError is raised when there is an error in the syntax of the program.
# SyntaxError is raised when there is an error in the syntax of the program.

try:
    print("Hello World")
except SyntaxError:
    print("SyntaxError")

# 2 Exceptions: It occur when unexpected things happen during execution of a program, even if the code is syntactically correct.

# Handling Exceptions
#try catch statement
try:
    x = int(input("Enter a number: "))
except ValueError:
    print("Invalid input")


while True:
    try:
        x = int(input("Enter a number: "))
        break
    except ValueError:
        print("Invalid input")
    except KeyboardInterrupt:
        print("Exiting program")
        break
    finally:
        print("Attempted to convert input to an integer")

print()
def party_planner(cookies, people):
    leftovers = None
    num_each = None
    # TODO: Add a try-except block here to
    #       make sure no ZeroDivisionError occurs.
    try:
        num_each = cookies // people
        leftovers = cookies % people

    except ZeroDivisionError:
        print("You can't have 0 cookies!")

    return(num_each, leftovers)

# The main code block is below; do not edit this
lets_party = 'y'
while lets_party == 'y':

    cookies = int(input("How many cookies are you baking? "))
    people = int(input("How many people are attending? "))

    cookies_each, leftovers = party_planner(cookies, people)

    if cookies_each:  # if cookies_each is not None
        message = "\nLet's party! We'll have {} people attending, they'll each get to eat {} cookies, and we'll have {} left over."
        print(message.format(people, cookies_each, leftovers))

    lets_party = input("\nWould you like to party more? (y or n) ")


print()
# Accessing Error Messages
#except Exception as e:
#    print("Error occurred: {}".format(e))

# Accessing Error Messages
#except Exception as e:
#    print(e)
