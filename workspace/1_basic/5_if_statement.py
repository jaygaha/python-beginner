# if = Do some code only if a condition is met
# else = Do something else if the condition is not met

age = int(input("Enter your age: "))

if age >= 18:
    print("You are an adult.")
elif age >= 13:
    print("You are a teenager.")
elif age >= 3:
    print("You are a kid.")
else:
    print("You are a child.")