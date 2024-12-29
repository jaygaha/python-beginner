# String: a string is a sequence of characters

name = input("Enter your name: ")

# 1. len() method
result = len(name)

print(result)

# 2. find() method: returns the index of the first occurrence of the specified value
result = name.find(" ")

print(result)

# 3. rfind() method: returns the index of the last occurrence of the specified value

result = name.rfind("a")

print(result)

# 4.capitalize() method: converts the first character of a string to uppercase
result = name.capitalize()

print(result)

# 5. upper() method: converts a string to uppercase
result = name.upper()

print(result)

# 6. lower() method: converts a string to lowercase
result = name.lower()

print(result)

# 7.isdigit() method: returns True if all characters in the string are digits
result = name.isdigit()

print(result)

# 8. isalpha() method: returns True if all characters in the string are alphabets
result = name.isalpha()

print(result)

# 9. isalnum() method: returns True if all characters in the string are alphanumeric

result = name.isalnum()

print(result)

# 10. count() method: returns the number of times a specified value occurs in a string

result = name.count("a")

print(result)

# 11. replace() method: replaces a specified value with another value in a string
result = name.replace("a", "A")

print(result)

## help(str)  # to get all the string methods

print(help(str))  #