# Variable Scope: the parts of a program that a variable can be referenced or used from
#
# scope: local, global, builtin
#
# local: defined inside a function
# global: defined outside of any function
# builtin: defined by the Python interpreter
#
# scope rules:
# 1. local variables can be accessed by any function within the same
#
# 2. global variables can be accessed by any function
#
# 3. builtin variables can be accessed by any function


##############################################################################
# egg_count = 0

# def buy_eggs():
#     egg_count += 12 # purchase a dozen eggs ## UnboundLocalError

# buy_eggs()
#
# # Better way to do this:

egg_count = 0

def buy_eggs(count):
    return count + 12  # purchase a dozen eggs

egg_count = buy_eggs(egg_count)

print(egg_count)
