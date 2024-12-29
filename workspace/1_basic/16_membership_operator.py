# Membership operators: used to test whether a value or variable is found in sequence (string, list, tuple, set, or dictionery)
# 1. in
# 2. not in

word = "TOKYO"

letter = input("Guess a letter in the secred word: ").upper()

# in
if letter in word:
    print(f"There is a {letter}")
else:
    print(f"{letter} was not found")

print()

# not in

if letter not in word:
    print(f"{letter} was not found")
else:
    print(f"There is a {letter}")

print()

# set
students = {"Kawakita", "Tanaka", "Yamaguchi"}

student = input("Search student name: ").capitalize()

if student not in students:
    print(f"No student with this name {student}")
else:
    print(f"Found the student: {student}")

student

# Dictionery

grades = {"Kawakita": "A", "Tanaka": "B", "Yamaguchi": "C", "Sato" : "B"}

student = input("Search student name: ").capitalize()

if student in grades:
    print(f"{student}'s grade is {grades[student]}")
else:
    print(f"{student} was not found.")

print()

# email string
#
# email = "hello@gmail.com"
email = "hellogmail.com"


if "@" in email and "." in email:
    print("Valid email")
else:
    print("Invalid email")