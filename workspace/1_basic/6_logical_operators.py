# Logical operators: evaluate multiple expressions
# and, or, not
# and: True if both the operands are true
# or: True if either of the operands is true
# not: True if operand is false (complements the operand)

# OR
temp = 24
is_raining = False

if temp > 35 or temp < 0 or is_raining:
    print("It's not a good day to go out")
else:
    print("It's a good day to go out")


# AND
temp = -2
is_sunny = False

if temp > 26 and is_sunny:
    print("It's a hot day to go out")
    print("Don't forget to wear sunscreen")
elif temp <= 0 and is_sunny:
    print("It's a cold day to go out")
    print("Don't forget to wear a jacket")
# elif temp < 26 and temp > 0 and is_sunny:
elif  26 > temp > 0 and is_sunny:
    print("It's a good day to go out")
elif temp > 26 and not is_sunny:
    print("It's a hot day to go out")
    print("Don't forget to wear sunscreen & umbrella")
elif temp <= 0 and not is_sunny:
    print("It's a cold day to go out")
    print("Don't forget to wear a jacket")
elif  26 > temp > 0 and not is_sunny:
    print("It's a clody day to go out")
