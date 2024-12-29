# validate user input exercise
# 1. user name is no more than 10 characters
# 2. user name must not contain space
# 3. user name must not contain digits

username = input("Enter your username: ")

# 1. len() method
result = len(username)

if result > 10:
    print("Username must not exceed 10 characters")
# 2. find() method: returns the index of the first occurrence of the specified value
elif not username.find(" ") == -1:
    print("Username must not contain space")
elif not username.isalpha():
    print("Username must not contain digits")
else:
    print("Username is valid")
    print(f"Welcome, {username}")