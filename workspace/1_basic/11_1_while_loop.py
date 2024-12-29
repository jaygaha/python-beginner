# while loop: Execute code block as long as condition is true

name = input("Enter your name: ")

while name == "":
    print("Name is required")
    name = input("Enter your name: ")

print(f"Welcome, {name}")

age = int(input("Enter your age: "))

while age < 0:
    print("Age must be a positive number")
    age = int(input("Enter your age: "))

print(f"Age: {age}")


food = input("Enter your favorite food (q to quit): ")

while not food == "q":
    print(f"Your favorite food is {food}")
    food = input("Enter another favorite food (q to quit): ")

print("Goodbye!")

# with logical operator

num = int(input("Enter a number between 1-10: "))

while num < 1 or num > 10:
    print("Number must be between 1-10")
    num = int(input("Enter a number between 1-10: "))


    print(f"Your number: {num}")