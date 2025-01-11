# Boolean expression for condition
condition = (1 == 1) and (2 == 2)
print(condition)

# Quiz
altitude = 1000
speed = 250
propulsion = "Propeller"

print(altitude < 1000 and speed > 100)
print((propulsion == "Jet" or propulsion == "Turboprop") and speed < 300 and altitude > 20000)
print(not (speed > 400 and propulsion == "Propeller"))
print((altitude > 500 and speed > 100) or not propulsion == "Propeller")

# Quiz: Using Truth Values of Objects
points = 174

# establish the default prize value to None
prize = None

# use the points value to assign prizes to the correct prize names
if points <= 50:
    prize = "wooden rabbit"
elif points <= 150:
    prize = None
elif points <= 180:
    prize = "wafer-thin mint"
else:
    prize = "penguin"

## use the value of points to assign prize to the correct prize name
# if points <= 50:
#     prize = "wooden rabbit"
# elif 151 <= points <= 180:
#     prize = "wafer-thin mint"
# elif points >= 181:
#     prize = "penguin"

if (prize == None):
    result = ("Oh dear, no prize this time.")
else:
    result = ("Congratulations! You won a {}!".format(prize))

# if prize:
#     result = "Congratulations! You won a {}!".format(prize)
# else:
#     result = "Oh dear, no prize this time."

print(result)


