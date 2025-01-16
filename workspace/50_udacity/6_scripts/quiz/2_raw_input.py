# Raw input

# Ask the user for their name
# name = input("What is your name? ")

# Ask the user for their age
# age = int(input("What is your age? "))

# Ask the user for their favorite color
# color = input("What is your favorite color? ")

# print("Hello {}, you are {}  old and your favorite color is {}.".format(name, age, color))

# Generate messages
names = input("Enter names separated by commas: ")
assignments = input("Enter assignments separated by commas: ")
grades = input("Enter grades separated by commas: ")

# Process the input into lists
names = [name.title().strip() for name in names.split(',')]
assignments = [int(count.strip()) for count in assignments.split(',')]
grades = [float(grade.strip()) for grade in grades.split(',')]

## message string to be used for each student
## HINT: use .format() with this string in your for loop
message = "Hi {},\n\nThis is a reminder that you have {} assignments left to \
submit before you can graduate. You're current grade is {} and can increase \
to {} if you submit all assignments before the due date.\n\n"

# Loop through each student and print the message
for name, missing_assignments, current_grade in zip(names, assignments, grades):
    potential_grade = current_grade + 2 * missing_assignments
    print(message.format(name, missing_assignments, current_grade, potential_grade))

# Solution
names = input("Enter names separated by commas: ").title().split(",")
assignments = input("Enter assignment counts separated by commas: ").split(",")
grades = input("Enter grades separated by commas: ").split(",")

message = "Hi {},\n\nThis is a reminder that you have {} assignments left to \
submit before you can graduate. You're current grade is {} and can increase \
to {} if you submit all assignments before the due date.\n\n"

for name, assignment, grade in zip(names, assignments, grades):
    print(message.format(name, assignment, grade, int(grade) + int(assignment)*2))
