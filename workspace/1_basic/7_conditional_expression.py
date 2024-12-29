# Conditonal Expression: A one-line shortcut for an if-else statement(ternary operator)
# x if condition else y
# Syntax: value_if_true if condition else value_if_false

num = 5

print("Positive" if num > 0 else "Negative")  # Positive

result = "Even" if num % 2 == 0 else "Odd"

print(result)  # Odd

a = 10
b = 11

max_num = a if a > b else b

print(max_num)  # 11

min_num = a if a < b else b

print(min_num)  # 10

age = 17

status = "Adult" if age >= 18 else "Child"

print(status)  # Child

temp = 30

weather = "Hot" if temp > 20 else "Normal"

print(weather)  # Hot

user_role = "Admin" # Admin, User

access = "Allowed" if user_role == "Admin" else "Denied"

print(access)  # Allowed