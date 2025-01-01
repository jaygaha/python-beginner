# Exception: An event that interrupts the normal flow of the program's execution.
# ZeroDivisionError: Occurs when you try to divide by zero.
# SyntaxError: Occurs when Python encounters incorrect syntax.
# TypeError: Occurs when you try to combine two objects that are not compatible.
# ValueError: Occurs when a built-in operation or function receives an argument that has the right type but an inappropriate value.
#
# 1. try:, 2. except:, 3. else:, 4. finally:

try:
    number = int(input("Enter a number: "))
    print(1/number)
except ZeroDivisionError:
    print("You can't divide by zero.")
except ValueError:
    print("Please enter a valid number.")
except Exception:
    print("Something went wrong.")
finally:
    print("This will always run.")
